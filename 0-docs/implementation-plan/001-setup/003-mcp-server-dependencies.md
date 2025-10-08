# 001-setup/003: MCP Server Dependencies Setup

## Goal
Initialize Node.js environment for MCP server with TypeScript.

## Steps

1. **Create mcp-server package.json**
   ```bash
   cd mcp-server/
   npm init -y
   ```

2. **Install MCP SDK and dependencies**
   ```bash
   npm install @modelcontextprotocol/sdk
   npm install ws  # WebSocket support
   npm install --save-dev typescript @types/node @types/ws
   npm install --save-dev tsx  # TypeScript execution
   ```

3. **Create tsconfig.json**
   - Target ES2022 (Node.js 18+)
   - Module CommonJS (for Node.js compatibility)
   - Strict mode enabled
   - Output to `dist/`

4. **Add npm scripts**
   - `build`: Compile TypeScript
   - `dev`: Run with tsx in watch mode
   - `start`: Run compiled JavaScript

## Acceptance Criteria

- [ ] package.json configured with MCP SDK
- [ ] TypeScript dependencies installed
- [ ] tsconfig.json for Node.js target
- [ ] Can compile TypeScript successfully

## ⚠️ File Size Reminder
**All source files created must be under 200 lines. NO EXCEPTIONS.**

## Dependencies
- Completes after: 001-project-structure

## Time Estimate
30 minutes
