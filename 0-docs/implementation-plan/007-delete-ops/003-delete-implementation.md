# 007-delete-ops/003: Implement deleteTask Operation

## Goal
Complete deleteTask end-to-end with confirmation flow.

## Steps

1. **Add to content/api/client.ts**
   - `deleteTask(taskId): Promise<void>`
   - Call Planner delete API
   - Handle response (may be 204 No Content)
   - Verify deletion (optional: check task no longer exists)

2. **Add to content/messaging.ts**
   - Handler for "DELETE_TASK" message
   - Validate taskId
   - Call API client
   - Return success/failure

3. **Update background/handlers.ts**
   - `handleDeleteTask` implementation
   - Validate taskId
   - Send to content script
   - Forward response to transport

4. **Update mcp-server/src/tools/deleteTask.ts**
   - Implement confirmation flow (from 002)
   - If not confirmed:
     - Fetch task details via getTasks
     - Return ConfirmationRequired
   - If confirmed:
     - Send delete message via transport
     - Return success

5. **Error handling**
   - Task not found (may already be deleted)
   - User lacks permission to delete
   - Network errors during delete
   - Handle gracefully with clear messages

6. **Add logging**
   - Log all delete attempts (confirmed and unconfirmed)
   - Include taskId, title in logs
   - Log deletion success
   - This creates audit trail

## Acceptance Criteria

- [ ] Delete requires confirmation
- [ ] Shows task details before delete
- [ ] Confirmed delete works
- [ ] Task disappears from Planner UI
- [ ] Errors handled gracefully
- [ ] Audit trail in logs
- [ ] **CRITICAL**: All modified files under 200 lines

## Dependencies
- Completes after: 007-delete-ops/002-confirmation-mechanism

## Time Estimate
1.5 hours

## Testing
- Attempt delete without confirmation
- Confirm and complete delete
- Try delete on non-existent task
- Try delete on task you don't own
- Verify logging
