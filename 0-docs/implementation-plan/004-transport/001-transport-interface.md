# 004-transport/001: Transport Layer Interface

## Goal
Define abstract transport interface for extension ↔ MCP server communication.

## Steps

1. **Create transport structure**
   ```
   mcp-server/src/transport/
   ├── index.ts           # Transport interface export
   ├── types.ts           # Transport types
   └── websocket.ts       # WebSocket implementation (next step)
   ```

2. **Implement transport/types.ts** (<100 lines)
   ```typescript
   - TransportMessage interface
   - TransportConnection interface
   - TransportOptions interface
   - MessageHandler type
   ```

3. **Define abstract Transport interface** in types.ts
   ```typescript
   interface Transport {
     connect(): Promise<void>
     disconnect(): Promise<void>
     send(message: TransportMessage): Promise<void>
     onMessage(handler: MessageHandler): void
     isConnected(): boolean
   }
   ```

4. **Define message format** in types.ts
   ```typescript
   interface TransportMessage {
     id: string           // Request/response correlation
     type: string         // Operation type
     payload: unknown     // Operation data
     timestamp: number
   }
   ```

5. **Create barrel export** in index.ts

## Acceptance Criteria

- [ ] Transport interface defined
- [ ] Message format specified
- [ ] Types exported from index.ts
- [ ] Interface is implementation-agnostic
- [ ] **CRITICAL**: All under 100 lines per file (well below 200-line limit)

## Dependencies
- Completes after: 001-setup/004-shared-types

## Time Estimate
45 minutes

## Architecture Notes
- Interface follows Dependency Inversion (SOLID)
- Implementations (WebSocket, etc.) depend on this interface
- Makes transport layer swappable without changing consumers
