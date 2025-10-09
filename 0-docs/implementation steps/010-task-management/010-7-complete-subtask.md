# 010-7: Complete Subtask

## API
```
PATCH /planner/tasks/{taskId}/details
Headers: If-Match: {etag}
Body: {
  "checklist": {
    "{itemId}": { "isChecked": true }
  }
}
```

## CLI Command
```bash
planner complete-subtask --task "Implement auth" --subtask "Write tests" [--plan "Engineering"]
```

## Python Function
```python
def complete_subtask(task_id: str, subtask_title: str, token: str) -> dict:
    details = get_json(f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details", token)
    etag = details["@odata.etag"]
    checklist = details.get("checklist", {})

    # Find by title
    item_id = None
    for cid, item in checklist.items():
        if item.get("title", "").lower() == subtask_title.lower():
            item_id = cid
            break

    if not item_id:
        raise ValueError(f"Subtask '{subtask_title}' not found")

    checklist[item_id]["isChecked"] = True

    return patch_json(
        f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details",
        token,
        {"checklist": checklist},
        etag
    )
```

## MCP Tool
```typescript
{
  name: "planner_completeSubtask",
  inputSchema: {
    type: "object",
    properties: {
      task: { type: "string" },
      subtask: { type: "string" },
      plan: { type: "string" }
    },
    required: ["task", "subtask"]
  }
}
```

## Test Cases
- [ ] Complete subtask by title
- [ ] Already completed is no-op
- [ ] Nonexistent subtask returns error
