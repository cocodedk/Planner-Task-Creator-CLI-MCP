# 004-transport/003: WebSocket Transport Client (Extension)

## Goal
Implement WebSocket client in extension background script.

## Steps

1. **Create transport module in extension**
   ```
   extension/src/background/transport/
   ├── index.ts           # Transport client
   ├── websocket.ts       # WebSocket implementation
   ├── messageQueue.ts    # Message queuing for reliability
   └── types.ts           # Client-specific types
   ```

2. **Implement websocket.ts** (<200 lines)
   - Connect to MCP server WebSocket
   - Reconnection logic with backoff
   - Message send/receive
   - Connection state management

3. **Implement messageQueue.ts** (<150 lines)
   - Queue messages when disconnected
   - Flush queue on reconnection
   - Handle message timeouts
   - Return promises for responses

4. **Request/response correlation**
   ```typescript
   - Generate unique message IDs
   - Track pending requests
   - Match responses to requests
   - Timeout handling
   ```

5. **Integration with background/handlers.ts**
   - Route handler calls to transport
   - Wait for responses
   - Handle transport errors

6. **Configuration**
   - WebSocket server URL in constants
   - Reconnection parameters
   - Timeout values

## Acceptance Criteria

- [ ] Extension connects to MCP server on startup
- [ ] Can send messages and receive responses
- [ ] Handles disconnections gracefully
- [ ] Reconnects automatically with backoff
- [ ] All files under 200 lines

## Dependencies
- Completes after: 004-transport/002-websocket-server, 002-extension/002-background-scaffold

## Time Estimate
2.5 hours

## Testing
- Start MCP server
- Load extension
- Verify WebSocket connection established
- Test message round-trip
- Test reconnection (restart server)
