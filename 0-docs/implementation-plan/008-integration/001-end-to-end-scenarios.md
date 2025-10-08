# 008-integration/001: End-to-End Scenario Testing

## Goal
Test complete user workflows using AI agent + MCP + extension.

## Test Scenarios

### Scenario 1: List and Read
1. User asks: "What plans do I have?"
2. AI calls getPlans
3. Verify plans listed
4. User asks: "What tasks are in Plan X?"
5. AI calls getTasks
6. Verify tasks listed with details

### Scenario 2: Create and Verify
1. User asks: "Create a task 'Write docs' due tomorrow in Plan X"
2. AI calls createTask with appropriate fields
3. Verify task created
4. AI calls getTasks to confirm
5. User checks Planner UI manually

### Scenario 3: Update and Verify
1. User asks: "Mark task Y as complete"
2. AI calls updateTask with status
3. Verify task updated
4. AI calls getTasks to confirm
5. User checks Planner UI manually

### Scenario 4: Delete with Confirmation
1. User asks: "Delete task Y"
2. AI calls deleteTask (first attempt)
3. System returns confirmation request with details
4. AI presents details to user
5. User confirms
6. AI calls deleteTask with confirmation
7. Verify task deleted

### Scenario 5: Error Handling
1. User asks: "Get tasks for invalid plan"
2. AI calls getTasks with bad planId
3. Verify clear error message returned
4. AI communicates error to user

### Scenario 6: Complex Workflow
1. List plans
2. Create new task
3. Update task multiple times
4. Mark complete
5. Create another task
6. Delete first task
7. Verify final state

## Testing Checklist

- [ ] All scenarios execute successfully
- [ ] Operations complete in < 3s each
- [ ] Errors are clear and actionable
- [ ] UI reflects all changes
- [ ] No extension errors in console
- [ ] No MCP server errors in logs
- [ ] AI agent receives proper responses
- [ ] **CRITICAL**: Verify all files still under 200 lines

## Dependencies
- Completes after: 007-delete-ops/004-delete-polish

## Time Estimate
2-3 hours

## Notes
Test with real AI agent (Cursor or similar). Document any UX issues discovered.
