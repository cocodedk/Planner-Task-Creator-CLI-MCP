# Environment Setup Guide

This guide explains how to manage your Azure AD credentials securely.

## Quick Answer

**For Cursor MCP usage:** You need to add credentials to `~/.config/Cursor/mcp.json`

**For CLI testing/development:** You can use a `.env` file or export environment variables

## Why Both?

### The Flow:
```
Cursor → mcp.json (env section) → MCP Server → Python CLI
```

The MCP server needs the credentials to be passed as environment variables, which is configured in the `mcp.json` file.

## Setup Methods

### Method 1: Cursor MCP (Required for Cursor Integration)

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

### Method 2: .env File (For Local Development)

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

### Method 3: Export Variables (Quick Testing)

```bash
export TENANT_ID="your-tenant-id"
export CLIENT_ID="your-client-id"
export PLANNER_DEFAULT_PLAN="FITS"
export PLANNER_DEFAULT_BUCKET="To do"

python planner.py list-plans
```

## Security Best Practices

### ✅ DO:
- ✅ Keep credentials in `~/.config/Cursor/mcp.json` (not in repo)
- ✅ Use `.env` file for local development (already in `.gitignore`)
- ✅ Use `.env.example` as a template (safe to commit)
- ✅ Set file permissions: `chmod 600 ~/.config/Cursor/mcp.json`

### ❌ DON'T:
- ❌ Commit `.env` files to git
- ❌ Hardcode credentials in scripts
- ❌ Share your `mcp.json` file publicly
- ❌ Include credentials in documentation

## Files Overview

| File | Purpose | Committed to Git? |
|------|---------|-------------------|
| `.env.example` | Template with placeholder values | ✅ Yes (safe) |
| `.env` | Your actual credentials | ❌ No (in .gitignore) |
| `~/.config/Cursor/mcp.json` | Cursor MCP configuration | ❌ No (in home dir) |
| `~/.planner-cli/config.json` | CLI configuration cache | ❌ No (in home dir) |
| `~/.planner-cli/msal_cache.bin` | Auth token cache | ❌ No (in home dir) |

## Which Method Should I Use?

### For Cursor AI Integration:
→ **Method 1** (mcp.json) - Required

### For CLI Development/Testing:
→ **Method 2** (.env file) - Recommended
→ **Method 3** (export) - Quick testing

### For Both:
You can use **both** methods simultaneously:
- Use `mcp.json` for Cursor
- Use `.env` file for CLI testing

## Getting Your Credentials

### Tenant ID:
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory**
3. Click **Properties**
4. Copy the **Tenant ID**

### Client ID:
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Find your app: "Planner Task Creator CLI"
4. Copy the **Application (client) ID**

## Updating Setup Scripts

If you've already run setup scripts with placeholder values, update them:

```bash
# Edit the mcp.json with your actual credentials
nano ~/.config/Cursor/mcp.json

# Then restart Cursor
```

## Troubleshooting

### "TENANT_ID and CLIENT_ID required"

**Cause:** Credentials not loaded in environment

**Solutions:**
- For Cursor: Check `~/.config/Cursor/mcp.json` has correct values
- For CLI: Export variables or load `.env` file
- Verify with: `echo $TENANT_ID` and `echo $CLIENT_ID`

### "Configuration file already exists"

**Cause:** Running setup script when mcp.json exists

**Solution:**
```bash
# Option 1: Edit existing file
nano ~/.config/Cursor/mcp.json

# Option 2: Backup and recreate
mv ~/.config/Cursor/mcp.json ~/.config/Cursor/mcp.json.backup
./scripts/setup-cursor-mcp.sh
```

## Summary

**The key point:** The MCP server needs credentials passed through `mcp.json`'s `env` section because that's how Cursor spawns the server with the necessary environment variables. A `.env` file is useful for CLI development but doesn't automatically provide variables to the MCP server.
