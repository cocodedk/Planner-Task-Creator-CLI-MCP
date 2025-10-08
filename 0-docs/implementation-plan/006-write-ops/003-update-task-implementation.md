# 006-write-ops/003: Implement updateTask Operation

## Goal
Complete updateTask end-to-end with partial update support.

## Steps

1. **Add to content/api/client.ts**
   - `updateTask(taskId, updates): Promise<Task>`
   - Support partial updates (only changed fields)
   - Build request payload
   - Call Planner API
   - Parse response

2. **Add to content/api/parsers.ts**
   - `parseTaskUpdatePayload(updates)`
   - Convert from partial Task type to API format
   - Only include fields that are being updated
   - Handle field-specific API quirks

3. **Add update validation**
   - Validate taskId
   - Validate update fields individually
   - Allow partial updates (any subset of fields)
   - Validate date format if dueDate updated
   - Validate status enum if status updated

4. **Update content/messaging.ts**
   - Handler for "UPDATE_TASK" message
   - Validate input
   - Call API client
   - Return updated task

5. **Update background/handlers.ts**
   - `handleUpdateTask` implementation
   - Validate input
   - Send to content script
   - Forward response

6. **Update mcp-server/src/tools/updateTask.ts**
   - Replace stub
   - Validate schema (taskId required, updates object)
   - Send via transport
   - Return updated task

7. **Handle common update scenarios**
   - Update title only
   - Update due date only
   - Update status only (mark complete)
   - Update multiple fields at once

## Acceptance Criteria

- [ ] Can update individual fields
- [ ] Can update multiple fields at once
- [ ] Partial updates work correctly
- [ ] Changes reflect in Planner UI
- [ ] Returns updated task
- [ ] **CRITICAL**: All modified files under 200 lines

## Dependencies
- Completes after: 006-write-ops/002-create-task-implementation

## Time Estimate
2 hours

## Testing
- Update task title
- Update due date
- Mark task complete (status)
- Update multiple fields
- Verify changes in UI
