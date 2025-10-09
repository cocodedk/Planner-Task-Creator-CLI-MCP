# MCP Server Module Decisions

**Architecture**: Spawn Python CLI as child process rather than reimplementing Graph API calls.

**MCP Framework**: Use standard MCP SDK for Node.js/TypeScript.

**Process Management**: Use Node.js `child_process.spawn` to run CLI commands.

**Environment Variables**: Pass through auth and config via environment variables.

**Error Handling**: Parse JSON errors from CLI stdout/stderr, return as MCP error responses.

**Tool Design**:
- `planner.initAuth`: Returns verification URL and code for device flow
- `planner.createTask`: Full task creation with all options
- `planner.setDefaults`: Set default plan and bucket
- `planner.listPlans`: List available plans
- `planner.listBuckets`: List buckets for specific plan
