# 007-delete-ops/002: Delete Confirmation Mechanism

## Goal
Implement safety confirmation for delete operations.

## Approach

Given the destructive nature of delete, implement confirmation at MCP tool level.

## Steps

1. **Design confirmation flow**
   ```
   AI agent → deleteTask(taskId)
   MCP server → returns "confirmation required" status
   AI agent → presents task details to user
   User → confirms or cancels
   AI agent → deleteTask(taskId, confirmed=true)
   MCP server → executes delete
   ```

2. **Update shared/types/messages.ts**
   - Add ConfirmationRequired response type
   - Add confirmed parameter to delete requests

3. **Update mcp-server/src/tools/deleteTask.ts**
   - Check for `confirmed` parameter
   - If not present, fetch task details
   - Return ConfirmationRequired with task details
   - If confirmed=true, proceed with deletion

4. **Add confirmation response format**
   ```typescript
   interface ConfirmationRequired {
     requiresConfirmation: true
     action: 'deleteTask'
     details: {
       taskId: string
       title: string
       planName?: string
     }
     message: string  // "Are you sure you want to delete..."
   }
   ```

5. **Optional: Dry-run mode**
   - Add `dryRun` parameter
   - Returns what would be deleted without deleting
   - AI agent can use this for safety

## Acceptance Criteria

- [ ] First delete call returns confirmation request
- [ ] Includes task details for user review
- [ ] Confirmed delete proceeds
- [ ] Unconfirmed delete is rejected
- [ ] **CRITICAL**: All modified files under 200 lines

## Dependencies
- Completes after: 007-delete-ops/001-delete-api-research

## Time Estimate
1.5 hours

## Notes
This safety mechanism is critical. Better to err on side of caution.
Consider making confirmation opt-out rather than opt-in.
