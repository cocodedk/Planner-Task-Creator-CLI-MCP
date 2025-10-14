# Bucket Management - Specification

## Operation: Create Bucket

**Function**: `create_bucket_op(plan_id: str, name: str, token: str) -> dict`

**Request**:
```python
POST /planner/buckets
{
  "name": "Sprint 1",
  "planId": "abc123",
  "orderHint": " !"
}
```

**Response**:
```json
{
  "ok": true,
  "bucketId": "bucket123",
  "name": "Sprint 1",
  "planId": "abc123"
}
```

**Errors**: `InvalidPlan`, `BucketExists` (if Graph API enforces uniqueness)

---

## Operation: Delete Bucket

**Function**: `delete_bucket_op(bucket_id: str, token: str) -> dict`

**Flow**:
1. GET `/planner/buckets/{bucketId}` for ETag
2. DELETE `/planner/buckets/{bucketId}` with If-Match header

**Response**:
```json
{
  "ok": true,
  "bucketId": "bucket123"
}
```

**Errors**: `BucketNotFound`, `BucketNotEmpty`, `ETagConflict`

---

## Operation: Update Bucket (Rename)

**Function**: `update_bucket_op(bucket_id: str, new_name: str, token: str) -> dict`

**Flow**:
1. GET `/planner/buckets/{bucketId}` for ETag
2. PATCH `/planner/buckets/{bucketId}` with new name and If-Match header
3. Retry once on 412 (ETag conflict)

**Response**:
```json
{
  "ok": true,
  "bucketId": "bucket123",
  "oldName": "Sprint 1",
  "newName": "Sprint 1 - Complete"
}
```

**Errors**: `BucketNotFound`, `ETagConflict`, `BucketExists` (name collision)

---

## Operation: Move Bucket Tasks

**Function**: `move_bucket_tasks_op(source_bucket_id: str, target_bucket_id: str, token: str) -> dict`

**Flow**:
1. GET `/planner/buckets/{sourceBucketId}/tasks`
2. For each task: call `move_task_op(task_id, target_bucket_id, token)`
3. Collect results

**Response**:
```json
{
  "ok": true,
  "moved": 5,
  "failed": 0,
  "taskIds": ["task1", "task2", "task3", "task4", "task5"],
  "errors": []
}
```

**Errors**: `BucketNotFound`, individual task move failures collected in `errors` array

---

## CLI Commands

### create-bucket
```bash
planner create-bucket --name "Sprint 1" --plan "My Project"
```

### delete-bucket
```bash
planner delete-bucket --bucket "Sprint 1" --plan "My Project"
```

### rename-bucket
```bash
planner rename-bucket --bucket "Sprint 1" --new-name "Sprint 1 - Complete" --plan "My Project"
```

### move-bucket-tasks
```bash
planner move-bucket-tasks --source "Sprint 1" --target "Sprint 2" --plan "My Project"
```

All commands output JSON for machine readability.
