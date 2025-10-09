# Configuration Setup

Open (or create) the `mcp.json` file and add the Planner server configuration:

```json
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": [
        "/absolute/path/to/your/project/dist/server.js"
      ],
      "env": {
        "TENANT_ID": "your-tenant-id-here",
        "CLIENT_ID": "your-client-id-here",
        "PLANNER_CLI_PATH": "/absolute/path/to/your/project/planner.py",
        "PLANNER_DEFAULT_PLAN": "FITS",
        "PLANNER_DEFAULT_BUCKET": "To do",
        "PYTHON_PATH": "/absolute/path/to/your/project/venv/bin/python"
      }
    }
  }
}
```

**Important Notes:**
- Use **absolute paths** (not relative paths like `~/` or `./`)
- Replace `/absolute/path/to/your/project` with your actual project path
- Replace `your-tenant-id-here` and `your-client-id-here` with your Azure AD credentials
- Set your default plan and bucket (optional but recommended)
