# Architecture Overview

This document describes the technical architecture of the Planner Task Creator CLI + MCP Server.

## Overview

The project consists of two main components:

1. **Python CLI** (`planner.py`): Standalone command-line interface
2. **MCP Server** (`src/server.ts`): Node.js wrapper for AI assistant integration

```
┌─────────────────────────────────────────────────────┐
│                   AI Assistant                       │
│              (Claude, Cursor, etc.)                  │
└───────────────────┬─────────────────────────────────┘
                    │ MCP Protocol
                    ▼
┌─────────────────────────────────────────────────────┐
│              MCP Server (Node.js/TS)                 │
│  - Tool definitions (planner_*)                      │
│  - Process management (spawn CLI)                    │
│  - JSON parsing and error handling                   │
└───────────────────┬─────────────────────────────────┘
                    │ stdio/subprocess
                    ▼
┌─────────────────────────────────────────────────────┐
│              Python CLI (planner.py)                 │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 001: Authentication                  │   │
│  │  - MSAL device code flow                     │   │
│  │  - Token caching with SerializableTokenCache │   │
│  │  - Cache file: ~/.planner-cli/msal_cache.bin │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 002: Graph API Client               │   │
│  │  - HTTP methods: GET, POST, PATCH           │   │
│  │  - Rate limiting (429 handling)             │   │
│  │  │  - Bearer token authentication              │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 003: Configuration Management       │   │
│  │  - Config file: ~/.planner-cli/config.json  │   │
│  │  - Precedence: CLI > Env > Config           │   │
│  │  - Secure file permissions (0600)           │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 004: Resolution                      │   │
│  │  - Name-to-ID mapping                        │   │
│  │  - Case-insensitive matching                 │   │
│  │  - GUID detection                            │   │
│  │  - Ambiguity detection                       │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 005: Task Creation                   │   │
│  │  - Task payload building                     │   │
│  │  - Label parsing (CSV → categories)          │   │
│  │  - Date formatting (ISO 8601)                │   │
│  │  - Description handling (ETag-based PATCH)   │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 006: CLI Commands                    │   │
│  │  - Typer-based CLI framework                 │   │
│  │  - Commands: init-auth, add, list-*, etc.   │   │
│  │  - Rich console output                       │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Module 007: Error Handling                  │   │
│  │  - Structured JSON errors                    │   │
│  │  - Error codes: NotFound, Ambiguous, etc.   │   │
│  │  - Candidate suggestions                     │   │
│  └─────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────┘
                    │ HTTPS (REST API)
                    ▼
┌─────────────────────────────────────────────────────┐
│         Microsoft Graph API (v1.0)                   │
│  - Endpoint: https://graph.microsoft.com/v1.0       │
│  - Resources: /planner/tasks, /planner/plans, etc.  │
│  - Authentication: OAuth 2.0 Bearer tokens          │
└─────────────────────────────────────────────────────┘
```
