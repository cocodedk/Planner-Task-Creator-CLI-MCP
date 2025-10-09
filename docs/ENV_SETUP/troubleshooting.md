# Troubleshooting

## "TENANT_ID and CLIENT_ID required"

**Cause:** Credentials not loaded in environment

**Solutions:**
- For Cursor: Check `~/.config/Cursor/mcp.json` has correct values
- For CLI: Export variables or load `.env` file
- Verify with: `echo $TENANT_ID` and `echo $CLIENT_ID`

## "Configuration file already exists"

**Cause:** Running setup script when mcp.json exists

**Solution:**
```bash
# Option 1: Edit existing file
nano ~/.config/Cursor/mcp.json

# Option 2: Backup and recreate
mv ~/.config/Cursor/mcp.json ~/.config/Cursor/mcp.json.backup
./scripts/setup-cursor-mcp.sh
```
