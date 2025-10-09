# 010-1: List Tasks

## API
```
GET /planner/plans/{planId}/tasks
GET /planner/buckets/{bucketId}/tasks
```

## CLI Command
```bash
planner list-tasks --plan "Engineering" [--bucket "Sprint 5"] [--incomplete]
```

## Python Function
```python
def list_tasks(token: str, plan_id: Optional[str] = None,
               bucket_id: Optional[str] = None,
               incomplete_only: bool = False) -> List[dict]:
    if bucket_id:
        url = f"{BASE_GRAPH_URL}/planner/buckets/{bucket_id}/tasks"
    elif plan_id:
        url = f"{BASE_GRAPH_URL}/planner/plans/{plan_id}/tasks"
    else:
        raise ValueError("plan_id or bucket_id required")

    data = get_json(url, token)
    tasks = data.get("value", [])

    if incomplete_only:
        tasks = [t for t in tasks if t.get("percentComplete", 0) < 100]

    return tasks
```

## MCP Tool
```typescript
{
  name: "planner_listTasks",
  inputSchema: {
    type: "object",
    properties: {
      plan: { type: "string" },
      bucket: { type: "string" },
      incompleteOnly: { type: "boolean" }
    },
    required: ["plan"]
  }
}
```

## Output Format
```json
[
  {
    "id": "abc-123",
    "title": "Task title",
    "bucketId": "bucket-id",
    "percentComplete": 0,
    "dueDateTime": "2025-10-15T17:00:00Z"
  }
]
```

## Test Cases
- [ ] List all tasks in plan
- [ ] List tasks in specific bucket
- [ ] Filter incomplete only
- [ ] Empty plan returns []
