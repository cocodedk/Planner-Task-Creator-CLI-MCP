# 010-2: Find Task

## Purpose
Resolve task identifier (ID or title) to full task object.

## Python Function
```python
def resolve_task(token: str, task: str,
                 plan_id: Optional[str] = None) -> dict:
    # GUID → fetch directly
    if GUID_PATTERN.match(task):
        return get_json(f"{BASE_GRAPH_URL}/planner/tasks/{task}", token)

    # Title → search
    if not plan_id:
        raise ValueError("plan_id required for title search")

    tasks = list_tasks(token, plan_id=plan_id)
    exact = case_insensitive_match(tasks, "title", task)

    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise_error("AmbiguousTask", candidates=exact)

    raise_error("TaskNotFound", candidates=tasks[:5])
```

## Error Handling
```json
{
  "code": "AmbiguousTask",
  "message": "Multiple tasks match 'Fix bug'",
  "candidates": [
    {"id": "...", "title": "Fix bug in auth"},
    {"id": "...", "title": "Fix bug in API"}
  ]
}
```

## MCP Tool
```typescript
{
  name: "planner_findTask",
  inputSchema: {
    type: "object",
    properties: {
      task: { type: "string", description: "Task ID or title" },
      plan: { type: "string" }
    },
    required: ["task", "plan"]
  }
}
```

## Test Cases
- [ ] Find by exact GUID
- [ ] Find by exact title match
- [ ] Ambiguous title returns candidates
- [ ] Not found returns candidates
- [ ] Case-insensitive matching
