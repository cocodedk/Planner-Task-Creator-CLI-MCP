# 010-6: List Subtasks

## API
```
GET /planner/tasks/{taskId}/details
```

## CLI Command
```bash
planner list-subtasks --task "Implement auth" [--plan "Engineering"]
```

## Python Function
```python
def list_subtasks(task_id: str, token: str) -> List[dict]:
    details = get_json(f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details", token)
    checklist = details.get("checklist", {})

    items = []
    for item_id, item_data in checklist.items():
        items.append({
            "id": item_id,
            "title": item_data.get("title"),
            "isChecked": item_data.get("isChecked", False)
        })

    return items
```

## Output Format
```json
[
  {
    "id": "abc-123",
    "title": "Write tests",
    "isChecked": false
  },
  {
    "id": "def-456",
    "title": "Update docs",
    "isChecked": true
  }
]
```

## MCP Tool
```typescript
{
  name: "planner_listSubtasks",
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
- [ ] List subtasks for task with checklist
- [ ] Empty checklist returns []
- [ ] Shows checked status correctly
