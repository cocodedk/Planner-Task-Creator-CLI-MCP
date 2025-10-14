# Bucket Management Implementation

## Summary
Add full bucket lifecycle management (CRUD + move tasks) to Planner CLI and MCP server.

## Operations
1. **Create Bucket** - Create new bucket in plan
2. **Delete Bucket** - Delete bucket by name/ID
3. **Rename Bucket** - Update bucket name
4. **Move Tasks** - Move all tasks from source to target bucket

## Files Created
- `planner_lib/bucket_create.py` (~40 lines)
- `planner_lib/bucket_delete.py` (~40 lines)
- `planner_lib/bucket_update.py` (~45 lines)
- `planner_lib/bucket_move.py` (~50 lines)
- `planner_lib/cli_bucket_commands.py` (~120 lines)
- `src/server/handlers-buckets.ts` (~110 lines)

## Files Modified
- `planner_lib/graph_client.py` - add `delete_json()`
- `planner.py` - register bucket commands
- `src/server/handlers.ts` - route bucket tools
- `src/server/tools.ts` - define bucket tools

## Testing Checklist

### Unit Tests
- [ ] `test_bucket_create.py` - create with valid/invalid plan
- [ ] `test_bucket_delete.py` - delete by ID/name, handle non-existent
- [ ] `test_bucket_update.py` - rename, ETag conflict retry
- [ ] `test_bucket_move.py` - move tasks, empty bucket, invalid target

### CLI Integration Tests
- [ ] Create bucket via CLI command
- [ ] Delete bucket via CLI command
- [ ] Rename bucket via CLI command
- [ ] Move tasks via CLI command
- [ ] Error handling (invalid plan, bucket not found)

### MCP Manual Tests
- [ ] `planner_createBucket` tool via Cursor
- [ ] `planner_deleteBucket` tool via Cursor
- [ ] `planner_renameBucket` tool via Cursor
- [ ] `planner_moveBucketTasks` tool via Cursor

## Usage Examples

### CLI
```bash
# Create bucket
planner create-bucket --name "Q1 Sprint" --plan "Product Roadmap"

# Rename bucket
planner rename-bucket --bucket "Q1 Sprint" --new-name "Q1 Complete" --plan "Product Roadmap"

# Move tasks
planner move-bucket-tasks --source "Q1 Sprint" --target "Archive" --plan "Product Roadmap"

# Delete bucket
planner delete-bucket --bucket "Q1 Complete" --plan "Product Roadmap"
```

### MCP (via AI assistant)
```
Create a bucket called "Sprint 1" in my Product Roadmap plan
Rename the "Backlog" bucket to "Icebox" in Product Roadmap
Move all tasks from "Sprint 1" to "Archive" in Product Roadmap
Delete the empty "Sprint 1" bucket from Product Roadmap
```

## Validation
Run `python 0-docs/bucket-management/verify_implementation.py` after implementation.
