# MCP Server Setup (Optional)

Only needed if you want to use with AI assistants like Claude.

## Step 1: Install Node Dependencies

```bash
npm install
```

## Step 2: Build TypeScript

```bash
npm run build
```

The compiled server will be in `dist/server.js`.

## Step 3: Configure MCP Client

For Claude Desktop, edit the config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Linux:** `~/.config/Claude/claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/full/path/to/planner-cli/dist/server.js"],
      "env": {
        "TENANT_ID": "your-tenant-id",
        "CLIENT_ID": "your-client-id",
        "PLANNER_DEFAULT_PLAN": "My Plan",
        "PLANNER_DEFAULT_BUCKET": "To Do",
        "PLANNER_CLI_PATH": "/full/path/to/planner.py"
      }
    }
  }
}
```

Replace `/full/path/to/` with actual absolute paths.

## Step 4: Restart Claude Desktop

Close and reopen Claude Desktop. The MCP server should now be available.
