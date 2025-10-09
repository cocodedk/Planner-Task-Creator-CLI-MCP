# Troubleshooting

## Issue: "Server failed to start"

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

## Issue: "Authentication failed"

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

## Issue: "Cannot find module"

**Solution:**
Ensure you've built the TypeScript:
```bash
cd /absolute/path/to/your/project
npm install
npm run build
```

## Issue: Python virtual environment not found

**Solution:**
Update the server to use full path to venv python. I'll create a wrapper script below.
