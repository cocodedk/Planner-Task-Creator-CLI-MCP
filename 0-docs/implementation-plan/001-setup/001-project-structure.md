# 001-setup/001: Initialize Project Structure

## Goal
Create root project structure with proper separation of extension and MCP server concerns.

## Steps

1. **Create root directory structure**
   ```
   Teams Planner MCP/
   ├── 0-docs/              # (already exists)
   ├── extension/           # Browser extension code
   ├── mcp-server/          # MCP server code
   ├── shared/              # Shared types between extension and server
   └── scripts/             # Build and development scripts
   ```

2. **Initialize Git repository** (if not done)
   - Add `.gitignore` for Node.js, TypeScript, build artifacts
   - Ignore `node_modules/`, `dist/`, `*.log`

3. **Create root README.md**
   - Project overview
   - Architecture diagram (text-based)
   - Quick start instructions (placeholder)

## Acceptance Criteria

- [ ] All directories created
- [ ] `.gitignore` in place
- [ ] Root README exists with basic structure

## ⚠️ File Size Reminder
**All source files created must be under 200 lines. NO EXCEPTIONS.**

## Dependencies
None - this is the first step.

## Time Estimate
15 minutes
