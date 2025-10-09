# Configuration Management Decisions

**File Format**: JSON for human readability and machine parsing.

**File Location**: `~/.planner-cli/config.json` (configurable via PLANNER_CONFIG_PATH env var).

**Security**: Set file permissions to 0600 (owner read/write only).

**Structure**:
```json
{
  "tenant_id": "azure-tenant-id",
  "client_id": "azure-client-id",
  "default_plan": "plan-name-or-id",
  "default_bucket": "bucket-name-or-id"
}
```

**Precedence Order** (highest to lowest):
1. CLI flags
2. Environment variables
3. Config file values
4. Prompt for missing required values

**Environment Variables**:
- `TENANT_ID`
- `CLIENT_ID`
- `PLANNER_DEFAULT_PLAN`
- `PLANNER_DEFAULT_BUCKET`
- `PLANNER_CONFIG_PATH`
