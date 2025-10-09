# MCP Server

## Implementation Details

**Lines of Code:** 250+
**Technology:** Node.js/TypeScript with MCP SDK
**Protocol:** Model Context Protocol (MCP)
**Process Management:** Spawns Python CLI as subprocess

## Core Features

- **Protocol Compliance**: Standard MCP implementation
- **Tool Definitions**: 5 tools for AI assistant integration
- **Process Management**: Secure subprocess spawning and management
- **Error Handling**: JSON parsing and structured error responses
- **Environment Management**: Credential passthrough to CLI

## MCP Tools Implemented

| Tool | Description | Parameters |
|------|-------------|------------|
| `planner_initAuth` | Initialize authentication | None |
| `planner_createTask` | Create task with options | title, plan?, bucket?, desc?, due?, labels?, assignee? |
| `planner_setDefaults` | Set default plan/bucket | plan, bucket |
| `planner_listPlans` | List available plans | None |
| `planner_listBuckets` | List buckets in plan | plan |

## Technical Architecture

- **TypeScript**: Full type safety and IntelliSense support
- **Process Management**: Isolated subprocess execution
- **JSON Communication**: Structured request/response handling
- **Environment Variables**: Secure credential management
