# Microsoft Planner Task Creator CLI + MCP Server

A command-line tool and MCP (Model Context Protocol) server for creating and managing Microsoft Planner tasks. This project provides both a standalone Python CLI and a Node.js MCP server wrapper for AI assistant integration.

**Created by:** [Babak Bandpey](https://cocode.dk)
**Website:** [cocode.dk](https://cocode.dk)

## Features

- 🔐 **Secure OAuth Authentication**: Device code flow with token caching
- 📋 **Task Management**: Create tasks with titles, descriptions, due dates, and labels
- 🎯 **Smart Resolution**: Case-insensitive plan and bucket name resolution
- ⚙️ **Flexible Configuration**: CLI flags, environment variables, and config file support
- 🤖 **MCP Integration**: Expose Planner functionality to AI assistants like Claude
- 🧪 **Comprehensive Testing**: Full test suite with pytest

## Architecture

```
┌─────────────────┐
│  AI Assistant   │
│ (Claude, etc.)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MCP Server     │
│  (Node.js/TS)   │
└────────┬────────┘
         │ spawns
         ▼
┌─────────────────┐
│  Python CLI     │
│  (planner.py)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Microsoft Graph │
│      API        │
└─────────────────┘
```

## Installation

### Prerequisites

- Python 3.8+ with pip
- Node.js 18+ with npm (for MCP server)
- Azure AD app registration with required permissions
- Access to Microsoft Planner

### Azure AD Setup

> **💡 Don't have an Azure subscription?** No problem! You don't need one. See [SETUP_WITHOUT_AZURE_SUBSCRIPTION.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION.md) for free options including the Microsoft 365 Developer Program.

1. Register an app in [Azure Portal](https://portal.azure.com)
2. Set redirect URI to `http://localhost` (Public client/native)
3. Add API permissions:
   - `Tasks.ReadWrite`
   - `Group.ReadWrite.All`
   - `offline_access`
4. Grant admin consent for permissions
5. Note your `Tenant ID` and `Client ID`

### Python CLI Setup

```bash
# Clone the repository
git clone <repo-url>
cd planner-task-creator-cli-mcp

# Install Python dependencies
pip install -r requirements.txt

# Make CLI executable
chmod +x planner.py

# Optional: Create symlink for global access
mkdir -p ~/.planner-cli
cp planner.py ~/.planner-cli/
ln -s ~/.planner-cli/planner.py /usr/local/bin/planner
```

### MCP Server Setup

```bash
# Install Node dependencies
npm install

# Build TypeScript
npm run build

# The compiled server will be in dist/server.js
```

## Configuration

### Environment Variables

```bash
export TENANT_ID="your-tenant-id"
export CLIENT_ID="your-client-id"
export PLANNER_DEFAULT_PLAN="My Plan"
export PLANNER_DEFAULT_BUCKET="To Do"
export PLANNER_CONFIG_PATH="~/.planner-cli/config.json"  # Optional
```

### Config File

Create `~/.planner-cli/config.json`:

```json
{
  "tenant_id": "your-tenant-id",
  "client_id": "your-client-id",
  "default_plan": "My Plan",
  "default_bucket": "To Do"
}
```

### Configuration Precedence

1. CLI flags (highest priority)
2. Environment variables
3. Config file
4. Prompt for missing values (lowest priority)

## Usage

### Python CLI

#### Initialize Authentication

```bash
python planner.py init-auth
```

This will display a device code and URL for authentication. Visit the URL and enter the code to complete authentication.

#### Set Default Plan and Bucket

```bash
python planner.py set-defaults --plan "My Plan" --bucket "To Do"
```

#### List Plans

```bash
python planner.py list-plans
```

#### List Buckets

```bash
python planner.py list-buckets --plan "My Plan"
```

#### Create a Task

**Minimal:**
```bash
python planner.py add --title "Complete project report"
```

**With all options:**
```bash
python planner.py add \
  --title "Complete project report" \
  --plan "Q4 Projects" \
  --bucket "In Progress" \
  --desc "Write and submit quarterly report with metrics" \
  --due "2024-12-31" \
  --labels "Label1,Label3" \
  --verbose
```

### MCP Server

#### Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/path/to/planner-mcp-server/dist/server.js"],
      "env": {
        "TENANT_ID": "your-tenant-id",
        "CLIENT_ID": "your-client-id",
        "PLANNER_DEFAULT_PLAN": "My Plan",
        "PLANNER_DEFAULT_BUCKET": "To Do"
      }
    }
  }
}
```

#### Available Tools

1. **planner_initAuth**: Initialize authentication
2. **planner_createTask**: Create a new task
3. **planner_setDefaults**: Set default plan and bucket
4. **planner_listPlans**: List available plans
5. **planner_listBuckets**: List buckets in a plan

## API Reference

### CLI Commands

#### `init-auth`
Initialize OAuth authentication with Microsoft.

**Usage:** `python planner.py init-auth`

#### `set-defaults`
Set default plan and bucket for task creation.

**Options:**
- `--plan TEXT`: Default plan name or ID (required)
- `--bucket TEXT`: Default bucket name or ID (required)

#### `list-plans`
List all available plans accessible to the user.

**Usage:** `python planner.py list-plans`

#### `list-buckets`
List all buckets in a specific plan.

**Options:**
- `--plan TEXT`: Plan name or ID (required)

#### `add`
Create a new task in Microsoft Planner.

**Options:**
- `--title TEXT`: Task title (required)
- `--plan TEXT`: Plan name or ID (optional if default is set)
- `--bucket TEXT`: Bucket name or ID (optional if default is set)
- `--desc TEXT`: Task description (optional)
- `--due TEXT`: Due date in YYYY-MM-DD format (optional)
- `--labels TEXT`: Comma-separated labels like "Label1,Label3" (optional)
- `--verbose`: Enable verbose output (optional)

### Label Format

Labels should be specified as comma-separated values: `Label1,Label2,Label3`

These are mapped to Planner categories:
- `Label1` → `category1`
- `Label2` → `category2`
- etc.

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=planner --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Project Structure

```
.
├── planner.py              # Main Python CLI
├── src/
│   └── server.ts          # MCP server implementation
├── tests/
│   ├── conftest.py        # Test fixtures
│   ├── test_auth.py       # Authentication tests
│   ├── test_config.py     # Configuration tests
│   ├── test_resolution.py # Resolution tests
│   ├── test_task_creation.py # Task creation tests
│   └── test_cli_commands.py  # CLI command tests
├── 0-docs/
│   ├── prd.md             # Product requirements
│   └── implementation steps/  # Detailed specs
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
└── README.md              # This file
```

### Module Overview

1. **Authentication (001)**: OAuth device code flow with MSAL
2. **Graph Client (002)**: HTTP client for Microsoft Graph API
3. **Configuration (003)**: Config file management
4. **Resolution (004)**: Plan and bucket name-to-ID resolution
5. **Task Creation (005)**: Task creation with all fields
6. **CLI Commands (006)**: Typer-based CLI interface
7. **Error Handling (007)**: Structured JSON error responses
8. **MCP Server (008)**: Node.js wrapper for AI integration
9. **Testing (009)**: Comprehensive test suite

## Error Handling

All errors are returned as structured JSON:

```json
{
  "code": "ErrorCode",
  "message": "Human-readable error message",
  "candidates": [{"id": "...", "name": "..."}]
}
```

### Error Codes

- `ConfigError`: Missing required configuration
- `NotFound`: Resource not found (with candidates)
- `Ambiguous`: Multiple matches (with candidates)
- `AuthError`: Authentication failure
- `UpstreamError`: Graph API error

## Security

- 🔐 Tokens are stored in `~/.planner-cli/msal_cache.bin` with 0600 permissions
- 🔒 Config file permissions are set to 0600
- 🚫 Tokens are never logged or exposed in output
- ✅ OAuth device code flow for secure authentication

## Troubleshooting

### Authentication Issues

**Problem:** Device code flow times out

**Solution:** Ensure you complete authentication within 15 minutes and have the required permissions

### Resolution Issues

**Problem:** "Plan not found" error

**Solution:** Use `list-plans` to see available plans. Plan names are case-insensitive but must match exactly.

**Problem:** "Multiple plans match" (Ambiguous)

**Solution:** Use the plan ID instead of name, or ensure unique naming

### Permission Issues

**Problem:** "Authorization failed: insufficient permissions"

**Solution:** Ensure your Azure AD app has the required API permissions and admin consent

### MCP Server Issues

**Problem:** MCP server not connecting

**Solution:**
1. Ensure Python CLI is working standalone first
2. Check that `PLANNER_CLI_PATH` points to correct location
3. Verify environment variables are set in MCP config

## Contributing

Contributions are welcome! Please:

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section
- Review the detailed specifications in `0-docs/implementation steps/`
- Open an issue on GitHub

## Author

**Babak Bandpey**
- Website: [cocode.dk](https://cocode.dk)
- Email: contact@cocode.dk

## Acknowledgments

- Microsoft Graph API for Planner integration
- MSAL Python library for authentication
- Typer and Rich for CLI framework
- MCP SDK for AI assistant integration
