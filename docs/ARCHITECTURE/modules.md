# Module Architecture

## Module 001: Authentication

**Purpose**: Secure OAuth authentication using MSAL device code flow

**Key Components**:
- `get_tokens(tenant_id, client_id) -> str`
- `msal.PublicClientApplication`
- `msal.SerializableTokenCache`

**Flow**:
1. Load cached token if available
2. Try silent token acquisition from cache
3. If no cache, initiate device code flow
4. Display verification URL and code to user
5. Poll for token acquisition
6. Save token to cache with 0600 permissions
7. Return access token

**Security**:
- Cache file: `~/.planner-cli/msal_cache.bin`
- Permissions: 0600 (owner read/write only)
- No tokens in logs or config files

## Module 002: Graph API Client

**Purpose**: HTTP client wrapper for Microsoft Graph API

**Key Functions**:
- `auth_headers(token) -> dict`
- `get_json(url, token) -> dict`
- `post_json(url, token, payload) -> dict`
- `patch_json(url, token, payload, etag) -> dict`

**Features**:
- Automatic retry on 429 (rate limiting)
- Bearer token authentication
- HTTP error handling with `raise_for_status()`
- Support for ETag-based optimistic concurrency

**Base URL**: `https://graph.microsoft.com/v1.0`

## Module 003: Configuration Management

**Purpose**: Configuration file and environment variable handling

**Key Functions**:
- `load_conf() -> dict`
- `save_conf(cfg: dict) -> None`
- `get_config_path() -> Path`

**Configuration Precedence** (highest to lowest):
1. CLI flags (e.g., `--plan "My Plan"`)
2. Environment variables (e.g., `PLANNER_DEFAULT_PLAN`)
3. Config file (`~/.planner-cli/config.json`)
4. Prompt/error for missing values

**Config Structure**:
```json
{
  "tenant_id": "string",
  "client_id": "string",
  "default_plan": "string",
  "default_bucket": "string"
}
```

## Module 004: Resolution

**Purpose**: Resolve plan and bucket names to IDs

**Key Functions**:
- `resolve_plan(token, plan) -> dict`
- `resolve_bucket(token, plan_id, bucket) -> dict`
- `list_user_plans(token) -> List[dict]`
- `list_plan_buckets(plan_id, token) -> List[dict]`
- `case_insensitive_match(items, key, value) -> List[dict]`

**Features**:
- GUID detection (bypass resolution if input is GUID)
- Case-insensitive name matching
- Ambiguity detection (multiple matches)
- Candidate suggestions on errors

**Error Types**:
- `NotFound`: No matches, return all candidates
- `Ambiguous`: Multiple matches, return matching candidates

## Module 005: Task Creation

**Purpose**: Create tasks with all supported fields

**Key Functions**:
- `create_task(token, plan_id, bucket_id, title, ...) -> dict`
- `parse_labels(labels_csv) -> Dict[str, bool]`

**Features**:
- Required fields: planId, bucketId, title
- Optional fields: dueDateTime, appliedCategories, description
- Label parsing: "Label1,Label3" → `{"category1": True, "category3": True}`
- Date formatting: "YYYY-MM-DD" → "YYYY-MM-DDTHH:MM:SSZ"
- Two-step description update (GET details for ETag, then PATCH)

**API Endpoints**:
- Create task: `POST /planner/tasks`
- Update details: `GET/PATCH /planner/tasks/{id}/details`

## Module 006: CLI Commands

**Purpose**: Typer-based command-line interface

**Commands**:
- `init-auth`: Initialize authentication
- `set-defaults`: Set default plan and bucket
- `list-plans`: List available plans
- `list-buckets`: List buckets in a plan
- `add`: Create a new task

**Framework**: Typer + Rich
- Typer: CLI framework with automatic help and type conversion
- Rich: Colored console output

**Output Format**: JSON for machine readability, Rich for human output

## Module 007: Error Handling

**Purpose**: Structured error responses

**Error JSON Format**:
```json
{
  "code": "ErrorCode",
  "message": "Human-readable message",
  "candidates": [{"id": "...", "name": "..."}],
  "details": "Additional context"
}
```

**Error Codes**:
- `ConfigError`: Missing configuration
- `AuthError`: Authentication failure
- `NotFound`: Resource not found
- `Ambiguous`: Multiple matches
- `RateLimited`: API rate limit
- `UpstreamError`: Graph API error

## Module 008: MCP Server

**Purpose**: Node.js/TypeScript MCP server wrapper

**Components**:
- `server.ts`: Main MCP server implementation
- Tool definitions: `planner_*` tools
- Process management: Spawn Python CLI as subprocess

**Tools**:
1. `planner_initAuth`: Initialize authentication
2. `planner_createTask`: Create task with all options
3. `planner_setDefaults`: Set defaults
4. `planner_listPlans`: List plans
5. `planner_listBuckets`: List buckets

**Implementation**:
```typescript
async function runCli(args: string[]): Promise<{code, stdout, stderr}>
async function handleToolCall(name: string, args: any): Promise<any>
```

**Transport**: stdio (standard input/output)
