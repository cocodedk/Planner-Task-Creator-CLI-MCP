# Architecture Documentation

This document describes the technical architecture of the Planner Task Creator CLI + MCP Server.

## Overview

The project consists of two main components:

1. **Python CLI** (`planner.py`): Standalone command-line interface
2. **MCP Server** (`src/server.ts`): Node.js wrapper for AI assistant integration

```
┌─────────────────────────────────────────────────────┐
│                   AI Assistant                       │
│              (Claude, Cursor, etc.)                  │
└───────────────────┬─────────────────────────────────┘
                    │ MCP Protocol
                    ▼
┌─────────────────────────────────────────────────────┐
│              MCP Server (Node.js/TS)                 │
│  - Tool definitions (planner_*)                      │
│  - Process management (spawn CLI)                    │
│  - JSON parsing and error handling                   │
└───────────────────┬─────────────────────────────────┘
                    │ stdio/subprocess
                    ▼
┌─────────────────────────────────────────────────────┐
│              Python CLI (planner.py)                 │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 001: Authentication                  │   │
│  │  - MSAL device code flow                     │   │
│  │  - Token caching with SerializableTokenCache │   │
│  │  - Cache file: ~/.planner-cli/msal_cache.bin │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 002: Graph API Client               │   │
│  │  - HTTP methods: GET, POST, PATCH           │   │
│  │  - Rate limiting (429 handling)             │   │
│  │  - Bearer token authentication              │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 003: Configuration Management       │   │
│  │  - Config file: ~/.planner-cli/config.json  │   │
│  │  - Precedence: CLI > Env > Config           │   │
│  │  - Secure file permissions (0600)           │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 004: Resolution                      │   │
│  │  - Name-to-ID mapping                        │   │
│  │  - Case-insensitive matching                 │   │
│  │  - GUID detection                            │   │
│  │  - Ambiguity detection                       │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 005: Task Creation                   │   │
│  │  - Task payload building                     │   │
│  │  - Label parsing (CSV → categories)          │   │
│  │  - Date formatting (ISO 8601)                │   │
│  │  - Description handling (ETag-based PATCH)   │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 006: CLI Commands                    │   │
│  │  - Typer-based CLI framework                 │   │
│  │  - Commands: init-auth, add, list-*, etc.   │   │
│  │  - Rich console output                       │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 007: Error Handling                  │   │
│  │  - Structured JSON errors                    │   │
│  │  - Error codes: NotFound, Ambiguous, etc.   │   │
│  │  - Candidate suggestions                     │   │
│  └─────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────┘
                    │ HTTPS (REST API)
                    ▼
┌─────────────────────────────────────────────────────┐
│         Microsoft Graph API (v1.0)                   │
│  - Endpoint: https://graph.microsoft.com/v1.0       │
│  - Resources: /planner/tasks, /planner/plans, etc.  │
│  - Authentication: OAuth 2.0 Bearer tokens          │
└─────────────────────────────────────────────────────┘
```

## Module Architecture

### Module 001: Authentication

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

### Module 002: Graph API Client

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

### Module 003: Configuration Management

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

### Module 004: Resolution

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

### Module 005: Task Creation

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

### Module 006: CLI Commands

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

### Module 007: Error Handling

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

### Module 008: MCP Server

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

## Data Flow

### Task Creation Flow

```
1. User/AI → MCP Tool Call → planner_createTask
                ↓
2. MCP Server → spawn CLI → python planner.py add --title "..."
                ↓
3. CLI → Load Config → Resolve tenant_id, client_id, plan, bucket
                ↓
4. CLI → get_tokens() → MSAL Authentication
                ↓
5. CLI → resolve_plan() → Graph API: GET /me/planner/plans
                ↓
6. CLI → resolve_bucket() → Graph API: GET /planner/plans/{id}/buckets
                ↓
7. CLI → create_task() → Graph API: POST /planner/tasks
                ↓
8. CLI → (if description) → Graph API: GET/PATCH /planner/tasks/{id}/details
                ↓
9. CLI → Output JSON → {"taskId": "...", "webUrl": "...", ...}
                ↓
10. MCP Server → Parse JSON → Return to AI Assistant
```

### Authentication Flow

```
1. CLI → get_tokens() → Check cache (~/.planner-cli/msal_cache.bin)
              ↓
2. If cached → acquire_token_silent() → Return token
              ↓
3. If no cache → initiate_device_flow() → Display code and URL
              ↓
4. User → Browser → Enter code → Authenticate
              ↓
5. CLI → acquire_token_by_device_flow() → Poll for token
              ↓
6. CLI → Save cache → Set permissions 0600 → Return token
```

## Testing Architecture

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── test_auth.py          # Authentication tests
├── test_config.py        # Configuration tests
├── test_resolution.py    # Resolution tests
├── test_task_creation.py # Task creation tests
└── test_cli_commands.py  # CLI integration tests
```

### Mock Strategy

- **MSAL**: Mock `PublicClientApplication` and `SerializableTokenCache`
- **Requests**: Mock `requests.get/post/patch` for Graph API calls
- **File System**: Use `tmp_path` fixtures for config and cache files

### Test Coverage

- Unit tests for individual functions
- Integration tests for CLI commands
- Mock external dependencies (MSAL, Graph API)
- Test all error paths and edge cases

## Security Considerations

### Token Security

- Tokens stored in `~/.planner-cli/msal_cache.bin` with 0600 permissions
- Tokens never logged or included in output
- Automatic token refresh via refresh tokens
- Cache encrypted by MSAL library

### Configuration Security

- Config file has 0600 permissions (owner only)
- Sensitive values (tenant_id, client_id) treated as confidential
- No hardcoded credentials in source code

### API Security

- OAuth 2.0 device code flow (no client secrets required)
- Required scopes explicitly declared
- Bearer token authentication for all API calls
- HTTPS for all Graph API communication

## Performance Considerations

### Caching

- Token caching reduces authentication overhead
- No caching of plans/buckets (always fetch fresh)
- Config file loaded once per CLI invocation

### Rate Limiting

- Automatic retry on 429 responses
- Respect `Retry-After` header
- Single retry attempt per request

### Optimization

- Minimal dependencies (msal, requests, typer, rich)
- Single-threaded synchronous execution
- Subprocess spawning for MCP server (isolated processes)

## Extensibility

### Adding New Commands

1. Define command function with `@app.command()` decorator
2. Add parameters with Typer options
3. Implement logic using existing modules
4. Output JSON for machine readability

### Adding New MCP Tools

1. Add tool definition to `TOOLS` array
2. Implement handler in `handleToolCall()`
3. Map MCP arguments to CLI arguments
4. Return parsed JSON output

### Adding New Graph API Endpoints

1. Use existing `get_json()`, `post_json()`, `patch_json()` functions
2. Handle specific endpoint quirks (ETag, pagination, etc.)
3. Add error handling for endpoint-specific errors

## Dependencies

### Python (CLI)

- `msal==1.30.0`: Microsoft Authentication Library
- `requests==2.32.3`: HTTP client library
- `typer==0.12.5`: CLI framework
- `rich==13.9.2`: Terminal formatting
- `pytest==8.3.3`: Testing framework
- `pytest-mock==3.14.0`: Mocking for pytest

### Node.js (MCP Server)

- `@modelcontextprotocol/sdk`: MCP protocol implementation
- `typescript`: Type-safe development
- `@types/node`: Node.js type definitions

## Deployment

### Python CLI Deployment

```bash
# System-wide installation
cp planner.py ~/.planner-cli/
ln -s ~/.planner-cli/planner.py /usr/local/bin/planner

# User installation
export PATH="$HOME/.planner-cli:$PATH"
```

### MCP Server Deployment

```bash
# Build
npm run build

# Configure in MCP client (e.g., Claude Desktop)
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/path/to/dist/server.js"],
      "env": { ... }
    }
  }
}
```

## Future Enhancements

Potential improvements:

1. **Assignee Resolution**: Add user email-to-ID resolution
2. **Task Updates**: Support updating existing tasks
3. **Batch Operations**: Create multiple tasks in one command
4. **Task Templates**: Save and reuse task templates
5. **Advanced Queries**: Search and filter tasks
6. **Attachment Support**: Add file attachments to tasks
7. **Comments**: Add comments to tasks
8. **Checklist Items**: Support subtasks/checklist items
9. **Web UI**: Optional web interface for task management
10. **Plugins**: Plugin system for custom integrations

## References

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
