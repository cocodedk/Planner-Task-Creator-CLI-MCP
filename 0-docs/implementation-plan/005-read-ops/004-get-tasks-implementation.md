# 005-read-ops/004: Implement getTasks Operation

## Goal
Complete getTasks end-to-end: MCP tool → extension → Planner API → response.

## Steps

1. **Update content/api/index.ts**
   - Implement real `getTasks(planId)`
   - Call Planner API with plan ID
   - Parse and return tasks

2. **Update content/messaging.ts**
   - Add handler for "GET_TASKS" message
   - Extract planId from message
   - Call API client
   - Return tasks to background

3. **Update background/handlers.ts**
   - Implement `handleGetTasks`
   - Validate planId input
   - Send message to content script
   - Forward response to transport

4. **Update mcp-server/src/tools/getTasks.ts**
   - Replace stub with real implementation
   - Validate input schema
   - Send message via transport
   - Return parsed tasks

5. **Input validation**
   - Validate planId is non-empty string
   - Validate planId format (if known)
   - Return clear error for invalid input

6. **Handle edge cases**
   - Empty plan (no tasks)
   - Invalid plan ID
   - Plan exists but user has no access

## Acceptance Criteria

- [ ] Can call getTasks with planId
- [ ] Returns real tasks from Planner
- [ ] Handles invalid planId gracefully
- [ ] Handles empty plans
- [ ] Response time < 3 seconds
- [ ] **CRITICAL**: All modified files under 200 lines

## Dependencies
- Completes after: 005-read-ops/003-get-plans-implementation

## Time Estimate
1 hour

## Testing
- Get a real planId from getPlans
- Call getTasks with that planId
- Verify tasks returned match UI
- Test with invalid planId
- Test with empty plan
