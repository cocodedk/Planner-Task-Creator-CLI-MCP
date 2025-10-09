# Data Flow

## Task Creation Flow

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

## Authentication Flow

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
