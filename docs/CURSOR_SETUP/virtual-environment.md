# Virtual Environment Setup

We need to modify the server to use the Python virtual environment.

## Option A: Set PYTHON_PATH in env (easier)
Already done in the config above - the server will use `python3` but we need to modify it slightly.

## Option B: Use the venv python directly
Modify the `spawn` command in `src/server.ts` to use the venv python.

Let's use Option B for reliability.

## Alternative - Use a Shell Script Wrapper

Create a wrapper script to ensure the Python virtual environment is used:

```bash
#!/bin/bash
# Location: /absolute/path/to/your/project/run-cli.sh

source /absolute/path/to/your/project/venv/bin/activate
exec python "$@"
```

Then update `mcp.json` to use this wrapper:

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
        "PYTHON_VENV": "/absolute/path/to/your/project/venv/bin/python"
      }
    }
  }
}
```
