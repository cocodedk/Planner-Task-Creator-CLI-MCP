# 010-4: Move Task

## API
```
PATCH /planner/tasks/{taskId}
Headers: If-Match: {etag}
Body: { "bucketId": "{newBucketId}" }
```

## CLI Command
```bash
planner move-task --task "Design review" --bucket "In Progress" [--plan "Engineering"]
```

## Python Function
```python
def move_task(task_id: str, bucket_id: str, token: str) -> dict:
    task = get_json(f"{BASE_GRAPH_URL}/planner/tasks/{task_id}", token)
    etag = task["@odata.etag"]

    return patch_json(
        f"{BASE_GRAPH_URL}/planner/tasks/{task_id}",
        token,
        {"bucketId": bucket_id},
        etag
    )
```

## MCP Tool
```typescript
{
  name: "planner_moveTask",
  inputSchema: {
    type: "object",
    properties: {
      task: { type: "string" },
      bucket: { type: "string" },
      plan: { type: "string" }
    },
    required: ["task", "bucket"]
  }
}
```

## Test Cases
- [ ] Move task to different bucket
- [ ] Bucket name resolution works
- [ ] Same bucket is no-op
- [ ] Invalid bucket returns error
