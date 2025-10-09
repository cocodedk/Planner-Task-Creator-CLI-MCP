# Setup Guide: Microsoft Planner Task Creator CLI + MCP Server

This guide walks you through the complete setup process from scratch.

> **💡 Don't have an Azure subscription?** You don't need one! Azure AD (Microsoft Entra ID) is free with Microsoft 365. See [SETUP_WITHOUT_AZURE_SUBSCRIPTION.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION.md) for detailed instructions on using:
> - Your work/school Microsoft 365 account
> - **Free Microsoft 365 Developer Program** (recommended for testing)
> - No Azure subscription required!

## Step 1: Azure AD App Registration

### 1.1 Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in:
   - **Name**: `Planner Task Creator CLI`
   - **Supported account types**: Choose based on your needs
   - **Redirect URI**: Select "Public client/native" and enter `http://localhost`
5. Click **Register**

### 1.2 Note Your IDs

After registration, note these values:
- **Application (client) ID**: Found on the Overview page
- **Directory (tenant) ID**: Found on the Overview page

### 1.3 Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph** → **Delegated permissions**
4. Add these permissions:
   - `Tasks.ReadWrite` - Read and write user and shared tasks
   - `Group.ReadWrite.All` - Read and write all groups (requires admin consent)
5. Click **Add permissions**
6. Click **Grant admin consent** (if you have admin rights)

**Note:** `Group.ReadWrite.All` requires admin consent. If you don't have admin rights, you can still use the tool with just `Tasks.ReadWrite` permission for basic functionality.

### 1.4 Configure Authentication

1. Go to **Authentication** in your app registration
2. Under **Advanced settings** → **Allow public client flows**: Set to **Yes**
3. Click **Save**

## Step 2: Install Prerequisites

### 2.1 Python Setup

Ensure Python 3.8 or later is installed:

```bash
python3 --version
```

If not installed, visit [python.org](https://www.python.org/downloads/)

### 2.2 Node.js Setup (for MCP server)

Ensure Node.js 18+ is installed:

```bash
node --version
npm --version
```

If not installed, visit [nodejs.org](https://nodejs.org/)

## Step 3: Install the Python CLI

### 3.1 Clone or Download

```bash
cd ~/projects
git clone <repo-url> planner-cli
cd planner-cli
```

Or if you have the files already, just navigate to the directory.

### 3.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or with a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3.3 Make CLI Accessible

**Option A: Direct execution**
```bash
chmod +x planner.py
```

**Option B: System-wide access**
```bash
# Create directory
mkdir -p ~/.planner-cli

# Copy CLI
cp planner.py ~/.planner-cli/

# Create symlink
sudo ln -s ~/.planner-cli/planner.py /usr/local/bin/planner

# Now you can run: planner --help
```

## Step 4: Configure the CLI

### 4.1 Set Environment Variables

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:

```bash
export TENANT_ID="your-tenant-id-here"
export CLIENT_ID="your-client-id-here"
export PLANNER_DEFAULT_PLAN="My Plan Name"  # Optional
export PLANNER_DEFAULT_BUCKET="To Do"       # Optional
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### 4.2 Or Create Config File

```bash
mkdir -p ~/.planner-cli

cat > ~/.planner-cli/config.json << 'EOF'
{
  "tenant_id": "your-tenant-id-here",
  "client_id": "your-client-id-here",
  "default_plan": "My Plan Name",
  "default_bucket": "To Do"
}
EOF

chmod 600 ~/.planner-cli/config.json
```

## Step 5: Test the CLI

### 5.1 Initialize Authentication

```bash
python planner.py init-auth
```

You should see:
```
Authentication Required
Please visit: https://microsoft.com/devicelogin
Enter code: ABCD1234
```

1. Open the URL in a browser
2. Enter the code shown
3. Complete the authentication flow
4. Return to your terminal

### 5.2 List Your Plans

```bash
python planner.py list-plans
```

You should see JSON output with your available plans.

### 5.3 Set Defaults

```bash
python planner.py set-defaults --plan "Your Plan Name" --bucket "Your Bucket Name"
```

### 5.4 Create a Test Task

```bash
python planner.py add --title "Test task from CLI"
```

You should see JSON output with the task ID and URL.

## Step 6: Install MCP Server (Optional)

Only needed if you want to use with AI assistants like Claude.

### 6.1 Install Node Dependencies

```bash
npm install
```

### 6.2 Build TypeScript

```bash
npm run build
```

The compiled server will be in `dist/server.js`.

### 6.3 Configure MCP Client

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

### 6.4 Restart Claude Desktop

Close and reopen Claude Desktop. The MCP server should now be available.

## Step 7: Verify Everything Works

### 7.1 Test CLI Directly

```bash
# List plans
python planner.py list-plans

# List buckets
python planner.py list-buckets --plan "Your Plan"

# Create task
python planner.py add \
  --title "Test task" \
  --desc "Testing the CLI" \
  --due "2024-12-31" \
  --labels "Label1" \
  --verbose
```

### 7.2 Test MCP Server (if installed)

In Claude Desktop, try asking:
```
"Can you create a task in my Planner called 'Test from Claude'?"
```

Claude should use the `planner_createTask` tool.

## Troubleshooting

### Issue: "TENANT_ID and CLIENT_ID required"

**Solution:** Ensure environment variables are set or config file exists with correct values.

```bash
echo $TENANT_ID
echo $CLIENT_ID
cat ~/.planner-cli/config.json
```

### Issue: Authentication fails immediately

**Solution:** Check Azure AD app configuration:
- Ensure "Allow public client flows" is enabled
- Verify API permissions are granted
- Try with a different browser for device login

### Issue: "Plan not found"

**Solution:**
1. Run `python planner.py list-plans` to see available plans
2. Use exact plan name (case-insensitive)
3. Or use plan ID instead of name

### Issue: MCP server not working

**Solution:**
1. Test CLI standalone first
2. Verify absolute paths in MCP config
3. Check Claude Desktop console for errors
4. Ensure Python 3 is in PATH

### Issue: Permission denied errors

**Solution:**
```bash
chmod 600 ~/.planner-cli/config.json
chmod 600 ~/.planner-cli/msal_cache.bin
chmod +x planner.py
```

### Issue: Module not found errors

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

## Next Steps

1. **Customize defaults**: Set your most-used plan and bucket as defaults
2. **Create aliases**: Add shell aliases for common operations
3. **Integrate with scripts**: Use the CLI in automation scripts
4. **Use with AI**: Leverage the MCP server with Claude for natural language task creation

## Example Workflow

```bash
# One-time setup
python planner.py init-auth
python planner.py set-defaults --plan "Work Projects" --bucket "To Do"

# Daily usage
python planner.py add --title "Review pull requests" --due "2024-12-20"
python planner.py add --title "Update documentation" --labels "Label2"
python planner.py add --title "Team meeting prep" --desc "Prepare agenda and slides"

# List tasks in different plan
python planner.py list-buckets --plan "Personal"
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
