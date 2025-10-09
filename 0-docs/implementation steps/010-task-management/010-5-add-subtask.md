# 010-5: Add Subtask

## API
```
PATCH /planner/tasks/{taskId}/details
Headers: If-Match: {etag}
Body: {
  "checklist": {
    "{newGuid}": { "title": "...", "isChecked": false, "orderHint": " !" }
  }
}
```

## CLI Command
```bash
planner add-subtask --task "Implement auth" --subtask "Write tests" [--plan "Engineering"]
```

## Python Function
```python
import uuid

def add_subtask(task_id: str, subtask_title: str, token: str) -> dict:
    details = get_json(f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details", token)
    etag = details["@odata.etag"]

    checklist = details.get("checklist", {})
    item_id = str(uuid.uuid4())
    checklist[item_id] = {
        "title": subtask_title,
        "isChecked": False,
        "orderHint": " !"
    }

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
  name: "planner_addSubtask",
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
- [ ] Add subtask to task
- [ ] Add multiple subtasks
- [ ] Task with no checklist initializes correctly
