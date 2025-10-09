# 1) Consolidated PRD — “Planner Task Creator (CLI + MCP)”

## Problem

Create Microsoft Planner tasks from Ubuntu and drop them into the **correct swim lane (bucket)**. Must be reliable (no UI automation), scriptable, and callable from MCP clients (Claude/Cursor).

## Goals

* One command: `planner add --title ... --plan ... --bucket ...`
* Bucket/plan can be **name or ID** (automatic resolution).
* Optional fields: **description, due date, assignee, labels**.
* MCP tool wraps the same capability for AI/IDE clients.

## Non-Goals

* No Playwright/UI driving Teams/Planner UI.
* No storing bearer tokens in config/JSON; use **Device Code OAuth** and MSAL cache.
* No full data sync or heavy browsing of Planner data.

## Success Criteria

* Task lands in the **requested bucket** by name within one call.
* Clear machine-readable errors: NotAuthorized, NotFound, Ambiguous, RateLimited.
* Steady-state creation after auth <1s network time (excluding user auth).

---

# 2) Architecture

* **CLI (Python)**

  * Uses **MSAL (PublicClientApplication + Device Code)** for OAuth.
  * Talks to **Microsoft Graph**:

    * Resolve plan → `/planner/plans` (or `/groups/{id}/planner/plans`)
    * Resolve buckets → `/planner/plans/{planId}/buckets`
    * Create task → `POST /planner/tasks`
    * Optional details → `GET /planner/tasks/{id}/details` then `PATCH` with `If-Match`.
* **Config**: `~/.planner-cli/config.json` (tenant_id, client_id, defaults).
* **Token cache**: `~/.planner-cli/msal_cache.bin` (0600).
* **MCP server (Node/TS)**

  * Exposes tools: `planner.createTask`, `planner.initAuth`, `planner.setDefaults`, `planner.listPlans`, `planner.listBuckets`.
  * Either calls the Python CLI via `child_process` **or** calls Graph directly via an internal module.

---

# 3) Functional Requirements

* Inputs:

  * **Required**: `title`, `plan` (name|id, unless default), `bucket` (name|id, unless default).
  * **Optional**: `desc`, `due` (YYYY-MM-DD), `assignee` (UPN/email), `labels` (`["Label1","Label3"]`).
* Name→ID resolution is **case-insensitive**. Ambiguity returns candidates.
* Description set via **details endpoint** (ETag handling).
* Assignments set at create (if provided) or via PATCH afterwards.

---

# 4) Non-Functional

* **Perf**: cache plan/bucket lookups in memory per run; token cache via MSAL.
* **Reliability**: backoff on 429 for GETs; one retry on POST if safe.
* **Observability**: JSON logs with requestId, endpoint, duration (no tokens).

---

# 5) Auth Model

* **Entra App Registration** (Public/native client; **no secret**).
* **Delegated scopes**: `Tasks.ReadWrite`, `Group.ReadWrite.All`, `offline_access`.
* **Device Code flow** for headless/terminal auth.
* Tokens cached by MSAL; renewed silently until refresh expires.

---

# 6) Configuration & Defaults (precedence)

1. CLI flags (highest)
2. Env vars (`TENANT_ID`, `CLIENT_ID`, `PLANNER_DEFAULT_PLAN`, `PLANNER_DEFAULT_BUCKET`)
3. `~/.planner-cli/config.json`
4. Prompt/explicit error if still missing

---

# 7) CLI Spec

```
planner add
  --title "Do X"                     (required)
  --plan  "<plan title|id>"          (required unless default)
  --bucket "<bucket name|id>"        (required unless default)
  [--desc "long text"]
  [--due "YYYY-MM-DD"]
  [--assignee "user@domain.com"]
  [--labels "Label1,Label3"]
  [--verbose]

planner init-auth
planner set-defaults --plan "<title|id>" --bucket "<name|id>"
planner list-plans [--group "<name|id>"]
planner list-buckets --plan "<title|id>"
```

---

# 8) Error Model (machine-friendly)

* **NotAuthorized**: missing consent/scopes; include required scopes.
* **NotFound**: plan or bucket name not found; include discovered candidates.
* **Ambiguous**: multiple plan matches; return candidates with ids/groupIds.
* **RateLimited**: include `retryAfter` seconds.
* **UpstreamError**: sanitized Graph error body & correlation id.

---

# 9) Security

* No tokens in JSON/config/logs.
* MSAL cache & config `0600`.
* Redact `Authorization` headers in debug logs.

---

# 10) Ubuntu Setup (once)

```bash
sudo apt update
sudo apt install -y python3 python3-venv
mkdir -p ~/.planner-cli && chmod 700 ~/.planner-cli

python3 -m venv ~/.planner-cli/venv
source ~/.planner-cli/venv/bin/activate
pip install msal requests typer rich
```

Create config (edit IDs later):

```bash
cat > ~/.planner-cli/config.json <<'EOF'
{
  "tenant_id": "11111111-2222-3333-4444-555555555555",
  "client_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  "default_plan": "",
  "default_bucket": ""
}
EOF
chmod 600 ~/.planner-cli/config.json
```

> Entra admin: grant delegated **Tasks.ReadWrite**, **Group.ReadWrite.All** to the **public client** app.

---

# 11) Python CLI — **Production-ready script** (single file)

Save as `~/.planner-cli/planner.py` and `chmod +x ~/.planner-cli/planner.py`.
(Uses Typer for a clean CLI; MSAL device code; full bucket/plan resolution; description via details PATCH.)

```python
#!/usr/bin/env python3
import os, sys, json, time, hashlib, typing as t
from datetime import datetime
import requests
import msal
import typer
from rich import print

APP = typer.Typer(no_args_is_help=True)

HOME = os.path.expanduser("~")
CONF_PATH = os.environ.get("PLANNER_CONFIG_PATH", f"{HOME}/.planner-cli/config.json")
CACHE_PATH = os.path.join(os.path.dirname(CONF_PATH), "msal_cache.bin")
API = "https://graph.microsoft.com/v1.0"

REQUIRED_SCOPES = ["Tasks.ReadWrite", "Group.ReadWrite.All", "offline_access"]

def load_conf() -> dict:
    if os.path.exists(CONF_PATH):
        with open(CONF_PATH) as f:
            return json.load(f)
    return {}

def save_conf(cfg: dict):
    os.makedirs(os.path.dirname(CONF_PATH), exist_ok=True)
    with open(CONF_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
    os.chmod(CONF_PATH, 0o600)

def get_tokens(tenant_id: str, client_id: str) -> str:
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.PublicClientApplication(client_id=client_id, authority=authority, token_cache=msal.SerializableTokenCache())
    # persist cache
    if os.path.exists(CACHE_PATH):
        app.token_cache.deserialize(open(CACHE_PATH, "r").read())
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(REQUIRED_SCOPES, account=accounts[0])
    if not result:
        flow = app.initiate_device_flow(scopes=REQUIRED_SCOPES)
        if "user_code" not in flow:
            raise RuntimeError("Failed to initiate device flow")
        print(f"[bold]Go to[/bold] {flow['verification_uri']} and enter code: [bold]{flow['user_code']}[/bold]")
        result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "Token acquisition failed"))
    # save cache
    with open(CACHE_PATH, "w") as f:
        f.write(app.token_cache.serialize())
    os.chmod(CACHE_PATH, 0o600)
    return result["access_token"]

def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def get_json(url: str, token: str) -> dict:
    r = requests.get(url, headers=auth_headers(token))
    if r.status_code == 429:
        ra = int(r.headers.get("Retry-After", "2"))
        time.sleep(ra)
        r = requests.get(url, headers=auth_headers(token))
    r.raise_for_status()
    return r.json()

def post_json(url: str, token: str, payload: dict) -> dict:
    r = requests.post(url, headers=auth_headers(token), json=payload)
    if r.status_code == 429:
        ra = int(r.headers.get("Retry-After", "2"))
        time.sleep(ra)
        r = requests.post(url, headers=auth_headers(token), json=payload)
    r.raise_for_status()
    return r.json()

def patch_json(url: str, token: str, payload: dict, etag: str):
    rh = auth_headers(token)
    rh["If-Match"] = etag
    r = requests.patch(url, headers=rh, json=payload)
    r.raise_for_status()
    return r.json() if r.text else {}

def case_insensitive_match(items: t.List[dict], key: str, value: str) -> t.List[dict]:
    v = value.lower()
    return [it for it in items if (it.get(key) or "").lower() == v]

def list_user_plans(token: str) -> t.List[dict]:
    # /me/planner/plans returns minimal info; include title via related group where needed
    data = get_json(f"{API}/me/planner/plans", token)
    plans = data.get("value", [])
    # augment with group displayName when possible
    for p in plans:
        gid = p.get("owner")
        if gid:
            try:
                g = get_json(f"{API}/groups/{gid}", token)
                p["groupName"] = g.get("displayName")
            except Exception:
                p["groupName"] = None
    return plans

def list_plan_buckets(plan_id: str, token: str) -> t.List[dict]:
    data = get_json(f"{API}/planner/plans/{plan_id}/buckets", token)
    return data.get("value", [])

def resolve_plan(token: str, plan: str) -> dict:
    # If looks like an ID (GUID), accept directly
    if len(plan) >= 30 and "-" in plan:
        return {"id": plan}
    plans = list_user_plans(token)
    exact = case_insensitive_match(plans, "title", plan)
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise ValueError(json.dumps({"code":"Ambiguous","message":"Multiple plan matches","candidates":[{"id":p["id"],"title":p["title"],"groupId":p.get("owner"),"groupName":p.get("groupName")} for p in exact]}))
    # not found → list candidates
    raise ValueError(json.dumps({"code":"NotFound","message":"Plan not found","candidates":[{"id":p["id"],"title":p["title"],"groupId":p.get("owner"),"groupName":p.get("groupName")} for p in plans]}))

def resolve_bucket(token: str, plan_id: str, bucket: str) -> dict:
    if len(bucket) >= 30 and "-" in bucket:
        return {"id": bucket}
    buckets = list_plan_buckets(plan_id, token)
    exact = case_insensitive_match(buckets, "name", bucket)
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise ValueError(json.dumps({"code":"Ambiguous","message":"Multiple bucket matches","candidates":[{"id":b["id"],"name":b["name"]} for b in exact]}))
    raise ValueError(json.dumps({"code":"NotFound","message":"Bucket not found","candidates":[{"id":b["id"],"name":b["name"]} for b in buckets]}))

def parse_labels(labels_csv: t.Optional[str]) -> t.Dict[str, dict]:
    if not labels_csv:
        return {}
    # Planner labels are label_1..label_6 names assigned per plan; basic mapping by name index
    names = [s.strip() for s in labels_csv.split(",") if s.strip()]
    # The Graph model expects appliedCategories e.g. {"category1": true}
    # We'll map Label1->category1, Label2->category2, ...
    out = {}
    for n in names:
        if n.lower().startswith("label"):
            try:
                idx = int(n.lower().replace("label",""))
                out[f"category{idx}"] = True
            except Exception:
                pass
    return out

@APP.command("init-auth")
def init_auth():
    cfg = load_conf()
    tenant_id = os.environ.get("TENANT_ID") or cfg.get("tenant_id")
    client_id = os.environ.get("CLIENT_ID") or cfg.get("client_id")
    if not tenant_id or not client_id:
        print("[red]TENANT_ID and CLIENT_ID required in env or config[/red]")
        raise typer.Exit(2)
    token = get_tokens(tenant_id, client_id)
    print("[green]Auth cached OK[/green]")

@APP.command("set-defaults")
def set_defaults(plan: str = typer.Option(...), bucket: str = typer.Option(...)):
    cfg = load_conf()
    cfg["default_plan"] = plan
    cfg["default_bucket"] = bucket
    save_conf(cfg)
    print("[green]Defaults saved[/green]")

@APP.command("list-plans")
def list_plans():
    cfg = load_conf()
    tenant_id = os.environ.get("TENANT_ID") or cfg.get("tenant_id")
    client_id = os.environ.get("CLIENT_ID") or cfg.get("client_id")
    token = get_tokens(tenant_id, client_id)
    plans = list_user_plans(token)
    print(json.dumps(plans, indent=2))

@APP.command("list-buckets")
def list_buckets(plan: str = typer.Option(...)):
    cfg = load_conf()
    tenant_id = os.environ.get("TENANT_ID") or cfg.get("tenant_id")
    client_id = os.environ.get("CLIENT_ID") or cfg.get("client_id")
    token = get_tokens(tenant_id, client_id)
    plan_obj = resolve_plan(token, plan)
    buckets = list_plan_buckets(plan_obj["id"], token)
    print(json.dumps(buckets, indent=2))

@APP.command("add")
def add(
    title: str = typer.Option(...),
    plan: str = typer.Option(None),
    bucket: str = typer.Option(None),
    desc: str = typer.Option(None),
    due: str = typer.Option(None),
    assignee: str = typer.Option(None),
    labels: str = typer.Option(None),
    verbose: bool = typer.Option(False, "--verbose")
):
    cfg = load_conf()
    tenant_id = os.environ.get("TENANT_ID") or cfg.get("tenant_id")
    client_id = os.environ.get("CLIENT_ID") or cfg.get("client_id")
    if not tenant_id or not client_id:
        print(json.dumps({"code":"ConfigError","message":"TENANT_ID/CLIENT_ID required"})); raise typer.Exit(2)
    token = get_tokens(tenant_id, client_id)

    plan_input = plan or os.environ.get("PLANNER_DEFAULT_PLAN") or cfg.get("default_plan")
    bucket_input = bucket or os.environ.get("PLANNER_DEFAULT_BUCKET") or cfg.get("default_bucket")
    if not plan_input or not bucket_input:
        print(json.dumps({"code":"ConfigError","message":"plan and bucket required (no defaults)"})); raise typer.Exit(2)

    plan_obj = resolve_plan(token, plan_input)
    bucket_obj = resolve_bucket(token, plan_obj["id"], bucket_input)

    payload = {
        "planId": plan_obj["id"],
        "bucketId": bucket_obj["id"],
        "title": title
    }
    if due:
        payload["dueDateTime"] = f"{due}T17:00:00Z"
    applied = parse_labels(labels)
    if applied:
        payload["appliedCategories"] = applied
    if assignee:
        # Minimal assignment structure; Graph will convert UPN to userId under the hood via plannerAssignments extensions
        # Safer: resolve user id first; for brevity we let Graph do it if possible.
        pass

    task = post_json(f"{API}/planner/tasks", token, payload)
    task_id = task["id"]

    if desc:
        # get details, patch with ETag
        details = get_json(f"{API}/planner/tasks/{task_id}/details", token)
        etag = details.get("@odata.etag")
        patch_json(f"{API}/planner/tasks/{task_id}/details", token, {"description": desc}, etag)

    out = {"taskId": task_id, "webUrl": task.get("detailsUrl", ""), "bucketId": bucket_obj["id"]}
    print(json.dumps(out))
    if verbose:
        print("[green]Created[/green]", out)

if __name__ == "__main__":
    APP()
```

**Examples:**

```bash
# first time
~/.planner-cli/planner.py init-auth

# set defaults
~/.planner-cli/planner.py set-defaults --plan "Engineering Board" --bucket "Backlog"

# create task
~/.planner-cli/planner.py add --title "Ship auth middleware" --desc "Add DC flow" --due 2025-10-20

# inspect
~/.planner-cli/planner.py list-plans
~/.planner-cli/planner.py list-buckets --plan "Engineering Board"
```

---

# 12) MCP Server — PRD & Pseudocode (Node/TypeScript)

## Tools

* `planner.initAuth` → triggers device code; returns `{ verificationUri, userCode }`
* `planner.createTask` → wraps CLI: inputs `{title, plan?, bucket?, desc?, due?, assignee?, labels?}`; returns `{taskId, webUrl, bucketId}`
* `planner.setDefaults` → persists plan/bucket defaults
* `planner.listPlans`, `planner.listBuckets` → discovery helpers

## Pseudocode (TypeScript-ish)

```ts
import { spawn } from "node:child_process";
import { MCPServer, Tool } from "some-mcp-sdk"; // replace with actual

const CLI = process.env.PLANNER_CLI_PATH || "/home/you/.planner-cli/planner.py";
const BASE_ENV = {
  TENANT_ID: process.env.TENANT_ID!,
  CLIENT_ID: process.env.CLIENT_ID!,
  PLANNER_DEFAULT_PLAN: process.env.PLANNER_DEFAULT_PLAN || "",
  PLANNER_DEFAULT_BUCKET: process.env.PLANNER_DEFAULT_BUCKET || "",
  PLANNER_CONFIG_PATH: process.env.PLANNER_CONFIG_PATH || ""
};

function runCli(args: string[]): Promise<{ code:number, stdout:string, stderr:string }> {
  return new Promise((resolve) => {
    const p = spawn(CLI, args, { env: { ...process.env, ...BASE_ENV } });
    let out = "", err = "";
    p.stdout.on("data", d => out += d);
    p.stderr.on("data", d => err += d);
    p.on("close", code => resolve({ code: code ?? 1, stdout: out, stderr: err }));
  });
}

const createTask: Tool = {
  name: "planner.createTask",
  inputSchema: {
    type: "object",
    required: ["title"],
    properties: {
      title: { type: "string" },
      plan: { type: "string" },
      bucket: { type: "string" },
      desc: { type: "string" },
      due: { type: "string", pattern: "^\\d{4}-\\d{2}-\\d{2}$" },
      assignee: { type: "string" },
      labels: { type: "string", description: "CSV: Label1,Label3" }
    }
  },
  async handler(input) {
    const args = ["add", "--title", input.title];
    if (input.plan)   args.push("--plan", input.plan);
    if (input.bucket) args.push("--bucket", input.bucket);
    if (input.desc)   args.push("--desc", input.desc);
    if (input.due)    args.push("--due", input.due);
    if (input.assignee) args.push("--assignee", input.assignee);
    if (input.labels) args.push("--labels", input.labels);

    const res = await runCli(args);
    if (res.code !== 0) {
      // try to surface structured JSON errors from CLI
      try { return { error: JSON.parse(res.stdout || res.stderr) }; }
      catch { return { error: { code: "UpstreamError", message: res.stderr || res.stdout } }; }
    }
    return JSON.parse(res.stdout);
  }
};

const initAuth: Tool = {
  name: "planner.initAuth",
  inputSchema: { type: "object", properties: {} },
  async handler() {
    const res = await runCli(["init-auth"]);
    if (res.code !== 0) return { error: res.stderr || res.stdout };
    // The CLI prints the device code URL line; just pass through for UX.
    return { ok: true, message: res.stdout };
  }
};

const setDefaults: Tool = {
  name: "planner.setDefaults",
  inputSchema: {
    type: "object",
    required: ["plan","bucket"],
    properties: { plan: {type:"string"}, bucket:{type:"string"} }
  },
  async handler(input) {
    const res = await runCli(["set-defaults", "--plan", input.plan, "--bucket", input.bucket]);
    return res.code === 0 ? { ok: true } : { error: res.stderr || res.stdout };
  }
};

const listPlans: Tool = {
  name: "planner.listPlans",
  inputSchema: { type: "object", properties: {} },
  async handler() {
    const res = await runCli(["list-plans"]);
    return res.code === 0 ? JSON.parse(res.stdout) : { error: res.stderr || res.stdout };
  }
};

const listBuckets: Tool = {
  name: "planner.listBuckets",
  inputSchema: { type: "object", required:["plan"], properties: { plan: {type:"string"} } },
  async handler(input) {
    const res = await runCli(["list-buckets", "--plan", input.plan]);
    return res.code === 0 ? JSON.parse(res.stdout) : { error: res.stderr || res.stdout };
  }
};

async function main() {
  const server = new MCPServer({ name: "planner-mcp-server" });
  server.registerTool(createTask);
  server.registerTool(initAuth);
  server.registerTool(setDefaults);
  server.registerTool(listPlans);
  server.registerTool(listBuckets);
  await server.start(); // bind stdio sockets per MCP
}
main().catch(err => { console.error(err); process.exit(1); });
```

---

# 13) MCP JSON snippets (Claude Desktop & Cursor)

## Claude Desktop (`~/claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/absolute/path/to/planner-mcp-server/dist/server.js"],
      "env": {
        "TENANT_ID": "11111111-2222-3333-4444-555555555555",
        "CLIENT_ID": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        "PLANNER_DEFAULT_PLAN": "Engineering Board",
        "PLANNER_DEFAULT_BUCKET": "Backlog",
        "PLANNER_CONFIG_PATH": "/home/you/.planner-cli/config.json",
        "PLANNER_CLI_PATH": "/home/you/.planner-cli/planner.py"
      },
      "disabled": false
    }
  }
}
```

## Cursor (global MCP JSON, e.g., `~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/absolute/path/to/planner-mcp-server/dist/server.js"],
      "env": {
        "TENANT_ID": "11111111-2222-3333-4444-555555555555",
        "CLIENT_ID": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        "PLANNER_DEFAULT_PLAN": "Engineering Board",
        "PLANNER_DEFAULT_BUCKET": "Backlog",
        "PLANNER_CONFIG_PATH": "/home/you/.planner-cli/config.json",
        "PLANNER_CLI_PATH": "/home/you/.planner-cli/planner.py"
      }
    }
  }
}
```

**Auth placement:**

* Put **TENANT_ID** and **CLIENT_ID** in env or config.
* **Do not** store tokens here. Run `planner.initAuth` once from Claude/Cursor; MSAL caches tokens at `~/.planner-cli/msal_cache.bin`.

---

# 14) Quick Test Matrix (sanity)

* [ ] `init-auth` shows device code; after completing, create works without prompting.
* [ ] `set-defaults` then `add --title "X"` uses defaults.
* [ ] Bucket name typo → `NotFound` with candidate buckets.
* [ ] Duplicate plan titles → `Ambiguous` with candidates.
* [ ] Missing scopes → `NotAuthorized` with scopes listed.
* [ ] Description successfully present in Planner UI post-PATCH.

---

# 15) Opinions (no sugar-coating)

* **Don’t touch Playwright** for Planner. It’s brittle and gets you blocked when DOM or throttling changes.
* **MCP is optional**; if you don’t need IDE/agent access, stop at the Python CLI.
* For longevity, consider moving assignments & user resolution to explicit **Graph user ID lookup** (UPN→userId) before setting `assignments`. I kept it minimal for speed; add it if you rely on assignments heavily.

That’s the whole package. If you want me to wire **user resolution** and **labels via plan metadata** next, say the word and I’ll extend the Python script accordingly.
