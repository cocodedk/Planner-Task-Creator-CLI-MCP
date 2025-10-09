# MCP Server Module Specification

**CLI Path**: Configurable via `PLANNER_CLI_PATH` env var, defaults to `~/.planner-cli/planner.py`

**Environment Variables**:
- `TENANT_ID`: Azure tenant ID
- `CLIENT_ID`: Azure client ID
- `PLANNER_DEFAULT_PLAN`: Default plan name/ID
- `PLANNER_DEFAULT_BUCKET`: Default bucket name/ID
- `PLANNER_CONFIG_PATH`: Custom config file path

**runCli Function**:
```typescript
function runCli(args: string[]): Promise<{ code: number, stdout: string, stderr: string }>
```

**Tool Specifications**:

**initAuth Tool**:
- Input: `{}` (no parameters)
- Process: Run `["init-auth"]`
- Output: `{ ok: true, message: stdout }` or `{ error: parsed_error }`

**createTask Tool**:
- Input: `{ title, plan?, bucket?, desc?, due?, assignee?, labels? }`
- Process: Build args array and run CLI
- Args: `["add", "--title", title, ...optional flags]`
- Output: Parsed JSON response or error

**setDefaults Tool**:
- Input: `{ plan, bucket }`
- Process: Run `["set-defaults", "--plan", plan, "--bucket", bucket]`
- Output: `{ ok: true }` or error

**listPlans Tool**:
- Input: `{}` (no parameters)
- Process: Run `["list-plans"]`
- Output: Parsed JSON array or error

**listBuckets Tool**:
- Input: `{ plan }`
- Process: Run `["list-buckets", "--plan", plan]`
- Output: Parsed JSON array or error

**Error Parsing**: Try to parse stdout as JSON error, fallback to stderr message.

**Server Setup**: Standard MCP server with stdio transport, register all tools.
