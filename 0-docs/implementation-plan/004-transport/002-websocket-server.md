# 004-transport/002: WebSocket Transport Server

## Goal
Implement WebSocket-based transport for MCP server side.

## Steps

1. **Implement transport/websocket.ts** (<200 lines)
   - Implement Transport interface
   - Use `ws` library
   - Handle connection lifecycle
   - Message serialization/deserialization

2. **Connection management**
   ```typescript
   - Track active connections
   - Handle connection/disconnection events
   - Heartbeat/keep-alive mechanism
   - Connection timeout handling
   ```

3. **Message handling**
   ```typescript
   - Receive messages from extension
   - Validate message format
   - Route to message handler
   - Send responses back
   ```

4. **Error handling**
   ```typescript
   - Connection errors
   - Message parsing errors
   - Network errors
   - Log all errors with context
   ```

5. **Create websocket utilities** in `transport/utils.ts` (<100 lines)
   - `generateMessageId()`
   - `serializeMessage()`
   - `deserializeMessage()`
   - `isValidMessage()`

6. **Integration with server**
   - Initialize WebSocket transport in server.ts
   - Pass transport to tool handlers

## Acceptance Criteria

- [ ] WebSocket server starts on configured port
- [ ] Can accept connections from clients
- [ ] Messages properly serialized/deserialized
- [ ] Connection lifecycle managed
- [ ] All files under 200 lines

## Dependencies
- Completes after: 004-transport/001-transport-interface

## Time Estimate
2 hours

## Testing
- Start WebSocket server
- Use WebSocket test client (e.g., `wscat`)
- Send test messages
- Verify responses
