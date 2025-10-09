# Summary

**The key point:** The MCP server needs credentials passed through `mcp.json`'s `env` section because that's how Cursor spawns the server with the necessary environment variables. A `.env` file is useful for CLI development but doesn't automatically provide variables to the MCP server.
