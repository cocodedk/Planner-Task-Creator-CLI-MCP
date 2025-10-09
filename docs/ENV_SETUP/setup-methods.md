# Setup Methods

## Method 1: Cursor MCP (Required for Cursor Integration)

**File:** `~/.config/Cursor/mcp.json`

```json
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/absolute/path/to/your/project/dist/server.js"],
      "env": {
        "TENANT_ID": "your-actual-tenant-id",
        "CLIENT_ID": "your-actual-client-id",
        "PLANNER_CLI_PATH": "/absolute/path/to/your/project/planner.py",
        "PLANNER_DEFAULT_PLAN": "FITS",
        "PLANNER_DEFAULT_BUCKET": "To do",
        "PYTHON_PATH": "/absolute/path/to/your/project/venv/bin/python"
      }
    }
  }
}
```

**Security Note:** This file is in your home directory and NOT committed to git.

## Method 2: .env File (For Local Development)

**Step 1:** Copy the example file:
```bash
cp .env.example .env
```

**Step 2:** Edit `.env` with your actual credentials:
```bash
# .env
TENANT_ID=your-actual-tenant-id
CLIENT_ID=your-actual-client-id
PLANNER_DEFAULT_PLAN=FITS
PLANNER_DEFAULT_BUCKET=To do
```

**Step 3:** Load environment variables before running CLI:
```bash
# Load .env variables
export $(cat .env | xargs)

# Now run CLI commands
python planner.py list-plans
```

Or use with a tool like `python-dotenv` or `direnv`.

## Method 3: Export Variables (Quick Testing)

```bash
export TENANT_ID="your-tenant-id"
export CLIENT_ID="your-client-id"
export PLANNER_DEFAULT_PLAN="FITS"
export PLANNER_DEFAULT_BUCKET="To do"

python planner.py list-plans
```
