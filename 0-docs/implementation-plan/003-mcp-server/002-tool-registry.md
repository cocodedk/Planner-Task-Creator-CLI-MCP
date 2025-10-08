# 003-mcp-server/002: Tool Registry Infrastructure

## Goal
Create tool registration system for MCP server.

## Steps

1. **Create tools structure**
   ```
   mcp-server/src/tools/
   ├── index.ts           # Tool registry
   ├── types.ts           # Tool interfaces
   └── schemas/           # JSON schemas for each tool
       └── index.ts       # Schema exports
   ```

2. **Implement tools/types.ts** (<100 lines)
   ```typescript
   - ToolDefinition interface
   - ToolHandler type
   - ToolResult<T> interface
   - ToolError interface
   ```

3. **Implement tools/index.ts** (<150 lines)
   - Tool registration mechanism
   - Tool lookup by name
   - Tool execution wrapper (error handling)
   - Tool list for MCP protocol

4. **Define tool schemas** in `schemas/`
   - JSON Schema for each tool's input
   - Start with stub schemas for MVP tools:
     - `getPlans`
     - `getTasks`
     - `createTask`
     - `updateTask`
     - `deleteTask`

5. **Integrate with server.ts**
   - Register tools on server startup
   - Connect tool execution to MCP handlers

## Acceptance Criteria

- [ ] Tool registry can register new tools
- [ ] Tool schemas validated on registration
- [ ] Can list all available tools
- [ ] Tool execution wrapped with error handling
- [ ] All files under 200 lines

## Dependencies
- Completes after: 003-mcp-server/001-server-scaffold

## Time Estimate
1.5 hours

## Architecture Notes
- Registry is separate from tool implementations
- Each tool implementation will be in its own file (next steps)
- Tool execution always returns ToolResult (success/error)
