# 006-write-ops/002: Implement createTask Operation

## Goal
Complete createTask end-to-end with validation and error handling.

## Steps

1. **Add to content/api/client.ts**
   - `createTask(planId, taskData): Promise<Task>`
   - Build request payload from taskData
   - Call Planner API
   - Parse response to Task type

2. **Add to content/api/parsers.ts**
   - `parseTaskCreatePayload(taskData)`
   - Convert from shared Task type to API format
   - Handle optional fields (dueDate, assignee, description)
   - Format dates correctly

3. **Add input validation**
   - Create `validateTaskInput()` in extension/src/shared/validation.ts
   - Required: planId, title
   - Optional but validated: dueDate (must be valid ISO date)
   - Title max length, description max length

4. **Update content/messaging.ts**
   - Handler for "CREATE_TASK" message
   - Validate input
   - Call API client
   - Return created task

5. **Update background/handlers.ts**
   - `handleCreateTask` implementation
   - Validate input
   - Send to content script
   - Forward response to transport

6. **Update mcp-server/src/tools/createTask.ts**
   - Replace stub
   - Validate JSON schema
   - Send via transport
   - Return created task

7. **Error handling**
   - Validation errors (client-side)
   - API errors (server-side)
   - Duplicate detection (if applicable)
   - Clear error messages

## Acceptance Criteria

- [ ] Can create task with required fields
- [ ] Can create task with optional fields
- [ ] Input validation works
- [ ] Task appears in Planner UI
- [ ] Returns created task with ID
- [ ] **CRITICAL**: All modified files under 200 lines

## Dependencies
- Completes after: 006-write-ops/001-write-api-research

## Time Estimate
2 hours

## Testing
- Create task with only title
- Create task with all fields
- Try invalid inputs (empty title, invalid date)
- Verify task appears in UI
