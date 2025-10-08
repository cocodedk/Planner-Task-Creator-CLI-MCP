# 005-read-ops/003: Implement getPlans Operation

## Goal
Complete getPlans end-to-end: MCP tool → extension → Planner API → response.

## Steps

1. **Update content/api/index.ts**
   - Implement real `getPlans()` using API client
   - Call Planner API
   - Parse and return plans

2. **Update content/messaging.ts**
   - Add handler for "GET_PLANS" message
   - Call API client
   - Return response to background

3. **Update background/handlers.ts**
   - Implement `handleGetPlans`
   - Send message to content script
   - Wait for response
   - Forward to transport (MCP server)

4. **Update mcp-server/src/tools/getPlans.ts**
   - Replace stub with real implementation
   - Send message via transport to extension
   - Wait for response
   - Return parsed data

5. **Error handling path**
   - Content script: wrap API errors
   - Background: handle content script errors
   - MCP server: format errors for AI agent

6. **Add logging**
   - Log each step in the chain
   - Log timing information
   - Log errors with full context

## Acceptance Criteria

- [ ] Can call getPlans from MCP client
- [ ] Returns real plans from Planner
- [ ] Errors handled at each layer
- [ ] Response time < 3 seconds
- [ ] Logging shows complete flow
- [ ] **CRITICAL**: All modified files under 200 lines

## Dependencies
- Completes after: 005-read-ops/002-api-client-module, 004-transport/004-end-to-end-test

## Time Estimate
1.5 hours

## Testing
- Start MCP server
- Load extension
- Navigate to Planner
- Use MCP client to call getPlans
- Verify actual plans returned
