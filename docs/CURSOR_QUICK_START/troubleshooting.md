# Troubleshooting

## MCP Server Not Working?

1. **Check Cursor's MCP status:**
   - Look for MCP server indicators in Cursor UI
   - Check Cursor's developer console (Help → Toggle Developer Tools)

2. **Test the CLI manually:**
   ```bash
   cd /absolute/path/to/your/project
   source venv/bin/activate
   python planner.py list-plans
   ```

3. **Test the MCP server:**
   ```bash
   cd /absolute/path/to/your/project
   ./scripts/test-mcp-server.sh
   ```

4. **Verify configuration:**
   ```bash
   cat ~/.config/Cursor/mcp.json
   ```

## Common Issues

**Issue:** "Server failed to start"
- **Fix:** Ensure Cursor was fully restarted (quit, don't just reload)
- **Fix:** Check that Node.js is installed: `node --version`
- **Fix:** Verify paths are absolute in `mcp.json`

**Issue:** "Authentication failed"
- **Fix:** Run `python planner.py init-auth` manually first
- **Fix:** Check token cache exists: `ls ~/.planner-cli/msal_cache.bin`

**Issue:** "Cannot find module"
- **Fix:** Rebuild the server: `npm run build`

**Issue:** "Python dependencies missing"
- **Fix:** Reinstall: `source venv/bin/activate && pip install -r requirements.txt`
