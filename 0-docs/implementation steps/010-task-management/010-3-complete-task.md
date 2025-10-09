# 010-3: Complete Task

## API
```
PATCH /planner/tasks/{taskId}
Headers: If-Match: {etag}
Body: { "percentComplete": 100 }
```

## CLI Command
```bash
planner complete-task --task "Fix bug" [--plan "Engineering"]
```

## Python Function
```python
def complete_task(task_id: str, token: str) -> dict:
    # Fetch current task for ETag
    task = get_json(f"{BASE_GRAPH_URL}/planner/tasks/{task_id}", token)
    etag = task["@odata.etag"]

    # Update with retry
    return patch_json(
        f"{BASE_GRAPH_URL}/planner/tasks/{task_id}",
        token,
        {"percentComplete": 100},
        etag
    )
```

## MCP Tool
```typescript
{
  name: "planner_completeTask",
  inputSchema: {
    type: "object",
    properties: {
      task: { type: "string" },
      plan: { type: "string" }
    },
    required: ["task"]
  }
}
```

## CLI Integration
```python
@app.command()
def complete_task(
    task: str = typer.Option(..., "--task"),
    plan: str = typer.Option(None, "--plan")
):
    cfg = load_conf()
    token = get_tokens(cfg["tenant_id"], cfg["client_id"])

    plan_id = None
    if plan or not GUID_PATTERN.match(task):
        plan_input = plan or cfg.get("default_plan")
        plan_obj = resolve_plan(token, plan_input)
        plan_id = plan_obj["id"]

    task_obj = resolve_task(token, task, plan_id)
    result = complete_task(task_obj["id"], token)
    print(json.dumps({"ok": True, "taskId": task_obj["id"]}))
```

## Test Cases
- [ ] Complete by task ID
- [ ] Complete by title
- [ ] Already complete returns success
- [ ] Invalid task returns error
