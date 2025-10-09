# Setting Up Planner MCP Server in Cursor

This guide shows you how to add the Microsoft Planner MCP server to Cursor editor.

## Prerequisites

✅ You've already completed:
- Python CLI is working
- Virtual environment is set up
- Authentication is configured
- Node dependencies are installed
- MCP server is built (`dist/server.js` exists)

## Step 1: Locate Your Cursor MCP Configuration File

The configuration file location depends on your operating system:

**Linux (your system):**
```bash
~/.config/Cursor/mcp.json
```

**macOS:**
```bash
~/Library/Application Support/Cursor/mcp.json
```

**Windows:**
```
%APPDATA%\Cursor\mcp.json
```

## Step 2: Create or Edit the Configuration File

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

## Step 3: Update the MCP Server to Use Virtual Environment

We need to modify the server to use the Python virtual environment. Let me update the server code:

**Option A: Set PYTHON_PATH in env (easier)**
Already done in the config above - the server will use `python3` but we need to modify it slightly.

**Option B: Use the venv python directly**
Modify the `spawn` command in `src/server.ts` to use the venv python.

Let's use Option B for reliability. I'll create an updated version.

## Step 4: Alternative - Use a Shell Script Wrapper

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

## Step 5: Restart Cursor

After saving the configuration:
1. **Completely quit Cursor** (not just close the window)
2. **Restart Cursor**
3. The MCP server will be loaded automatically

## Step 6: Verify It's Working

In Cursor's AI chat, you should be able to:

### Test 1: List Plans
```
Can you list my Microsoft Planner plans?
```

### Test 2: List Buckets
```
What buckets are in my FITS plan?
```

### Test 3: Create a Task
```
Create a task in my FITS plan called "Test from Cursor" in the To do bucket
```

## Available MCP Tools

Once configured, Cursor's AI will have access to these tools:

| Tool | Description | Example |
|------|-------------|---------|
| `planner_listPlans` | List all your plans | "Show my plans" |
| `planner_listBuckets` | List buckets in a plan | "What buckets are in FITS?" |
| `planner_createTask` | Create a new task | "Create a task..." |
| `planner_setDefaults` | Set default plan/bucket | "Set FITS as default" |
| `planner_initAuth` | Re-authenticate if needed | "Initialize Planner auth" |

## Troubleshooting

### Issue: "Server failed to start"

**Check the logs:**
Cursor may have MCP server logs. Look for error messages about:
- Missing `node` command
- Missing Python dependencies
- Authentication issues

**Solution:**
1. Verify paths in `mcp.json` are absolute
2. Test the server manually:
   ```bash
   cd /home/bba/0-projects/Planner\ Task\ Creator\ CLI\ MCP
   node dist/server.js
   ```
3. Check that Python virtual environment has all dependencies

### Issue: "Authentication failed"

**Solution:**
Run authentication manually first:
```bash
cd /absolute/path/to/your/project
source venv/bin/activate
export TENANT_ID="your-tenant-id-here"
export CLIENT_ID="your-client-id-here"
python planner.py init-auth
```

The cached token will be used by the MCP server.

### Issue: "Cannot find module"

**Solution:**
Ensure you've built the TypeScript:
```bash
cd /absolute/path/to/your/project
npm install
npm run build
```

### Issue: Python virtual environment not found

**Solution:**
Update the server to use full path to venv python. I'll create a wrapper script below.

## Quick Setup Script

Save this as `setup-cursor-mcp.sh`:

```bash
#!/bin/bash

PROJECT_DIR="/absolute/path/to/your/project"
CONFIG_DIR="$HOME/.config/Cursor"
CONFIG_FILE="$CONFIG_DIR/mcp.json"

echo "Setting up Planner MCP for Cursor..."

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Create the configuration
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": [
        "$PROJECT_DIR/dist/server.js"
      ],
      "env": {
        "TENANT_ID": "your-tenant-id-here",
        "CLIENT_ID": "your-client-id-here",
        "PLANNER_CLI_PATH": "$PROJECT_DIR/planner.py",
        "PLANNER_DEFAULT_PLAN": "FITS",
        "PLANNER_DEFAULT_BUCKET": "To do",
        "PYTHON_PATH": "$PROJECT_DIR/venv/bin/python"
      }
    }
  }
}
EOF

echo "✅ Configuration created at: $CONFIG_FILE"
echo ""
echo "Next steps:"
echo "1. Update PROJECT_DIR in this script with your actual path"
echo "2. Update TENANT_ID and CLIENT_ID with your Azure credentials"
echo "3. Restart Cursor completely"
echo "4. Test by asking: 'Can you list my Planner plans?'"
echo ""
echo "Configuration contents:"
cat "$CONFIG_FILE"
```

Run it:
```bash
chmod +x setup-cursor-mcp.sh
./setup-cursor-mcp.sh
```

## Testing Without Cursor

You can test the MCP server works using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector node dist/server.js
```

This will open a web interface where you can test the MCP tools.

## Summary

After setup, you'll be able to:
- ✅ Ask Cursor AI to create Planner tasks
- ✅ List your plans and buckets through conversation
- ✅ Set defaults and manage tasks via natural language
- ✅ All using the same authentication token from your CLI

**Example conversation in Cursor:**
```
You: "Create a task called 'Review code' in my FITS plan, To do bucket, due next Friday"

Cursor AI: [Uses planner_createTask tool]
"✅ Task created successfully! Task ID: xyz..."
```
