# Deployment

## Python CLI Deployment

```bash
# System-wide installation
cp planner.py ~/.planner-cli/
ln -s ~/.planner-cli/planner.py /usr/local/bin/planner

# User installation
export PATH="$HOME/.planner-cli:$PATH"
```

## MCP Server Deployment

```bash
# Build
npm run build

# Configure in MCP client (e.g., Claude Desktop)
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/path/to/dist/server.js"],
      "env": { ... }
    }
  }
}
```
