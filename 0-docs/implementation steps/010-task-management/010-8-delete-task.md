# 010-8: Delete Task

## API
```
DELETE /planner/tasks/{taskId}
Headers: If-Match: {etag}
```

## CLI Command
```bash
planner delete-task --task "Old task" --confirm [--plan "Engineering"]
```

## Python Function
```python
def delete_task(task_id: str, token: str) -> dict:
    task = get_json(f"{BASE_GRAPH_URL}/planner/tasks/{task_id}", token)
    etag = task["@odata.etag"]

    response = requests.delete(
        f"{BASE_GRAPH_URL}/planner/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "If-Match": etag
        }
    )
    response.raise_for_status()

    return {"ok": True, "taskId": task_id}
```

## CLI Integration
```python
@app.command()
def delete_task(
    task: str = typer.Option(..., "--task"),
    confirm: bool = typer.Option(False, "--confirm"),
    plan: str = typer.Option(None, "--plan")
):
    if not confirm:
        print(json.dumps({
            "code": "ConfirmationRequired",
            "message": "Add --confirm flag to delete task"
        }))
        raise typer.Exit(1)

    # ... resolve and delete
```

## MCP Tool
```typescript
{
  name: "planner_deleteTask",
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

## Test Cases
- [ ] Delete with --confirm flag succeeds
- [ ] Delete without --confirm fails
- [ ] MCP tool deletes directly (no flag needed)
- [ ] Invalid task returns error
