# Bucket Management - Decisions

## Architecture

### Modular Design (SOLID, SRP)
- **Separate operation files**: `bucket_create.py`, `bucket_delete.py`, `bucket_update.py`, `bucket_move.py`
- Each file <50 lines, single responsibility
- Follow existing patterns from `task_delete.py`, `task_move.py`

### Reuse Existing Components (DRY)
- Use `graph_client.py` for all HTTP operations
- Use `resolution_buckets.py` for bucket name → ID resolution
- Add `delete_json()` to graph_client for DELETE operations

### CLI Command Naming
- `create-bucket` - creates new bucket in plan
- `delete-bucket` - deletes bucket by name or ID
- `rename-bucket` - updates bucket name
- `move-bucket-tasks` - moves all tasks from source to target bucket

All commands require `--plan` for bucket resolution.

### MCP Tool Naming
- `planner_createBucket`
- `planner_deleteBucket`
- `planner_renameBucket`
- `planner_moveBucketTasks`

Match existing `planner_createTask` convention.

## Error Handling

### Error Codes
- `BucketNotFound` - bucket name/ID not found in plan
- `BucketExists` - bucket with same name already exists
- `InvalidPlan` - plan ID invalid or inaccessible
- `ETagConflict` - concurrent modification detected
- `BucketNotEmpty` - delete attempted on bucket with tasks

### Error Response Format
```json
{
  "code": "BucketNotFound",
  "message": "Bucket 'Sprint 1' not found in plan",
  "candidates": [
    {"id": "bucket123", "name": "Sprint 2"}
  ]
}
```

Match existing error format from `resolution_buckets.py`.

## ETag Handling
- Fetch current bucket for ETag before update/delete
- Include `If-Match` header in PATCH/DELETE requests
- Retry once on 412 Precondition Failed (ETag conflict)
- Pattern from `task_delete.py` and `task_move.py`

## Move Tasks Operation
- List all tasks in source bucket
- Update each task's `bucketId` to target bucket ID
- Reuse existing `task_move.py` logic
- Return summary: `{"moved": 5, "failed": 0, "taskIds": [...]}`

## MVP Scope (TAGNI)
- No bucket reordering (orderHint management)
- No metadata updates beyond name
- No cascading deletes (must be empty or use force flag)
- No bulk bucket operations
- No bucket templates or presets
