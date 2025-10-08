# 004-transport/004: Transport Layer End-to-End Test

## Goal
Verify complete communication path: MCP server ↔ Extension.

## Steps

1. **Create test scenario**
   - MCP server calls `getPlans` tool (stub)
   - Tool routes to extension via transport
   - Extension sends mock response
   - Response returns to MCP client

2. **Test infrastructure**
   - Start MCP server
   - Load extension in browser
   - Use MCP client (Cursor or test script)
   - Call tool and verify response

3. **Test cases**
   - ✓ Successful request/response
   - ✓ Request timeout
   - ✓ Connection lost during request
   - ✓ Invalid message format
   - ✓ Multiple concurrent requests

4. **Logging verification**
   - MCP server logs tool invocation
   - Transport logs message send
   - Extension logs message receive
   - Extension logs response send
   - MCP server logs response receive

5. **Performance check**
   - Measure round-trip time
   - Should be < 500ms on localhost
   - Log timing information

## Acceptance Criteria

- [ ] Can invoke tool from MCP client
- [ ] Response returns correctly
- [ ] All error cases handled
- [ ] Logs show complete message flow
- [ ] Round-trip time acceptable

## ⚠️ File Size Reminder
**All source files must remain under 200 lines. NO EXCEPTIONS.**

## Dependencies
- Completes after: 004-transport/003-websocket-client, 003-mcp-server/003-tool-stubs

## Time Estimate
1.5 hours

## Notes
This validates the entire transport layer before implementing real operations.
All subsequent work builds on this working foundation.
