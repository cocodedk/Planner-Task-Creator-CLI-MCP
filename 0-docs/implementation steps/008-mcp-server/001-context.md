# MCP Server Module Context

**Purpose**: Create Node.js/TypeScript MCP server that wraps the Python CLI.

**Scope**: Expose planner tools for AI/IDE clients (Claude, Cursor).

**Key Requirements**:
- Spawn Python CLI as child process
- Parse JSON output from CLI
- Handle device code flow for auth
- Expose tools: createTask, initAuth, setDefaults, listPlans, listBuckets
