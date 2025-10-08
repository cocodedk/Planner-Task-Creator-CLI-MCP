# 003-mcp-server/001: MCP Server Scaffold

## Goal
Create basic MCP server that starts and registers with MCP protocol.

## Steps

1. **Create server structure**
   ```
   mcp-server/src/
   ├── index.ts           # Entry point, server initialization
   ├── server.ts          # MCP Server instance configuration
   ├── config.ts          # Configuration management
   └── types.ts           # Server-specific types
   ```

2. **Implement index.ts** (<50 lines)
   - Load configuration
   - Initialize MCP server
   - Start server
   - Handle shutdown gracefully

3. **Implement server.ts** (<100 lines)
   - Create McpServer instance
   - Configure server info (name, version)
   - Register capabilities
   - Setup error handlers

4. **Implement config.ts** (<50 lines)
   - Load from environment variables
   - Server port configuration
   - WebSocket endpoint configuration
   - Validation of required config

5. **Create startup script**
   - Add `start.sh` in scripts/
   - Sets environment variables
   - Starts server with proper logging

## Acceptance Criteria

- [ ] Server starts without errors
- [ ] Responds to MCP protocol handshake
- [ ] Logs startup information
- [ ] Graceful shutdown on SIGTERM
- [ ] All files under 200 lines

## Dependencies
- Completes after: 001-setup/003-mcp-server-dependencies

## Time Estimate
1 hour

## Testing
- Start server: `npm run dev`
- Check logs for successful startup
- Verify MCP SDK connection (manual test with MCP client)
