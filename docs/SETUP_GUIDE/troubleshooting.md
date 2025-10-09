# Troubleshooting

## Issue: "TENANT_ID and CLIENT_ID required"

**Solution:** Ensure environment variables are set or config file exists with correct values.

```bash
echo $TENANT_ID
echo $CLIENT_ID
cat ~/.planner-cli/config.json
```

## Issue: Authentication fails immediately

**Solution:** Check Azure AD app configuration:
- Ensure "Allow public client flows" is enabled
- Verify API permissions are granted
- Try with a different browser for device login

## Issue: "Plan not found"

**Solution:**
1. Run `python planner.py list-plans` to see available plans
2. Use exact plan name (case-insensitive)
3. Or use plan ID instead of name

## Issue: MCP server not working

**Solution:**
1. Test CLI standalone first
2. Verify absolute paths in MCP config
3. Check Claude Desktop console for errors
4. Ensure Python 3 is in PATH

## Issue: Permission denied errors

**Solution:**
```bash
chmod 600 ~/.planner-cli/config.json
chmod 600 ~/.planner-cli/msal_cache.bin
chmod +x planner.py
```

## Issue: Module not found errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

To verify your installation:

```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-mock

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py
```

## Getting Help

- Review the main README.md for detailed documentation
- Check the specs in `0-docs/implementation steps/`
- Open an issue on GitHub
- Check Azure AD app permissions and configuration

## Security Notes

- Never commit your `config.json` or `.env` files
- Keep your tenant ID and client ID private
- Token cache file is automatically secured with 0600 permissions
- Regularly review your Azure AD app permissions
