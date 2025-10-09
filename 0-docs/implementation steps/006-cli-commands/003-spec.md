# CLI Commands Module Specification

**Command Definitions**:

**init-auth Command**:
- No parameters
- Load config for tenant_id, client_id
- Call get_tokens() and display success
- Handle config errors with JSON error output

**set-defaults Command**:
- Required: `--plan PLAN`, `--bucket BUCKET` (name or ID)
- Load current config, update default_plan and default_bucket
- Save config and display success message

**list-plans Command**:
- No parameters
- Load config and get auth token
- Call list_user_plans() and output as formatted JSON

**list-buckets Command**:
- Required: `--plan PLAN` (name or ID)
- Load config and get auth token
- Resolve plan to get plan_id
- Call list_plan_buckets(plan_id) and output as formatted JSON

**add Command**:
- Required: `--title TITLE`
- Optional: `--plan PLAN`, `--bucket BUCKET`, `--desc DESC`, `--due DUE`, `--assignee ASSIGNEE`, `--labels LABELS`, `--verbose`
- Resolve configuration (flags → env vars → config file)
- Validate required plan and bucket (or defaults)
- Resolve plan and bucket names/IDs
- Create task with all provided fields
- Output result as JSON (and verbose message if requested)

**Configuration Resolution Pattern** (for add command):
```python
plan_input = plan or os.environ.get("PLANNER_DEFAULT_PLAN") or cfg.get("default_plan")
bucket_input = bucket or os.environ.get("PLANNER_DEFAULT_BUCKET") or cfg.get("default_bucket")
if not plan_input or not bucket_input:
    # JSON error and exit
```

**Error Handling**: All commands output JSON errors and exit with code 2 for config issues.
