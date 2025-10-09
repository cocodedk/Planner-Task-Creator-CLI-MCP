# Documentation Index

Welcome to the Microsoft Planner Task Creator CLI + MCP Server documentation!

## 🚀 Getting Started

Start here if you're new to the project:

1. **[SETUP_WITHOUT_AZURE_SUBSCRIPTION.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION.md)** - ⭐ **No Azure subscription? Start here!**
2. **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
3. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions including Azure AD configuration
4. **[README.md](README.md)** - Main documentation with full feature list and usage

## 📖 Documentation

### User Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Step-by-step setup instructions
- **[README.md](README.md)** - Complete user manual with API reference
- **[EXAMPLES.md](EXAMPLES.md)** - Practical examples and real-world workflows

### Technical Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and design decisions
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Implementation summary and status

### Reference

- **[0-docs/prd.md](0-docs/prd.md)** - Product requirements document
- **[0-docs/implementation steps/](0-docs/implementation%20steps/)** - Detailed module specifications

## 🎯 Quick Links

### Installation

```bash
# Quick install
./INSTALLATION.sh

# Or manual install
pip install -r requirements.txt
cp planner.py ~/.planner-cli/
```

See: [SETUP_GUIDE.md](SETUP_GUIDE.md)

### First Steps

```bash
# 1. Authenticate
python planner.py init-auth

# 2. Set defaults
python planner.py set-defaults --plan "My Plan" --bucket "To Do"

# 3. Create task
python planner.py add --title "My first task"
```

See: [QUICKSTART.md](QUICKSTART.md)

### Common Tasks

```bash
# List plans
python planner.py list-plans

# List buckets
python planner.py list-buckets --plan "Work"

# Create task with details
python planner.py add \
  --title "Complete report" \
  --desc "Q4 metrics" \
  --due "2024-12-31" \
  --labels "Label1"
```

See: [EXAMPLES.md](EXAMPLES.md)

## 📂 Project Structure

```
planner-task-creator-cli-mcp/
├── planner.py              # Main Python CLI
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
├── INSTALLATION.sh        # Automated installer
│
├── src/
│   └── server.ts         # MCP server
│
├── tests/
│   ├── conftest.py       # Test fixtures
│   ├── test_auth.py      # Auth tests
│   ├── test_config.py    # Config tests
│   ├── test_resolution.py
│   ├── test_task_creation.py
│   └── test_cli_commands.py
│
├── 0-docs/
│   ├── prd.md            # Product requirements
│   └── implementation steps/
│       ├── 000-overview.md
│       ├── 001-authentication/
│       ├── 002-graph-client/
│       └── ... (9 modules total)
│
└── Documentation/
    ├── INDEX.md          # This file
    ├── README.md         # Main docs
    ├── QUICKSTART.md     # Quick start
    ├── SETUP_GUIDE.md    # Setup guide
    ├── EXAMPLES.md       # Examples
    ├── ARCHITECTURE.md   # Architecture
    └── PROJECT_SUMMARY.md # Summary
```

## 🔧 Development

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/test_auth.py

# With coverage
pytest --cov=planner
```

### Building MCP Server

```bash
npm install
npm run build
```

See: [ARCHITECTURE.md](ARCHITECTURE.md)

## 📚 Documentation by Topic

### Authentication

- Setup: [SETUP_GUIDE.md § Azure AD Setup](SETUP_GUIDE.md#step-1-azure-ad-app-registration)
- Usage: [README.md § Authentication](README.md#initialize-authentication)
- Architecture: [ARCHITECTURE.md § Module 001](ARCHITECTURE.md#module-001-authentication)
- Spec: [0-docs/implementation steps/001-authentication/](0-docs/implementation%20steps/001-authentication/)

### Configuration

- Setup: [SETUP_GUIDE.md § Configure the CLI](SETUP_GUIDE.md#step-4-configure-the-cli)
- Usage: [README.md § Configuration](README.md#configuration)
- Examples: [EXAMPLES.md § Configuration](EXAMPLES.md#configuration)
- Architecture: [ARCHITECTURE.md § Module 003](ARCHITECTURE.md#module-003-configuration-management)

### Task Creation

- Usage: [README.md § Create a Task](README.md#create-a-task)
- Examples: [EXAMPLES.md § Task Creation](EXAMPLES.md#task-creation)
- Architecture: [ARCHITECTURE.md § Module 005](ARCHITECTURE.md#module-005-task-creation)
- Spec: [0-docs/implementation steps/005-task-creation/](0-docs/implementation%20steps/005-task-creation/)

### MCP Server

- Setup: [SETUP_GUIDE.md § Install MCP Server](SETUP_GUIDE.md#step-6-install-mcp-server-optional)
- Usage: [README.md § MCP Server](README.md#mcp-server)
- Examples: [EXAMPLES.md § MCP Server Usage](EXAMPLES.md#mcp-server-usage)
- Architecture: [ARCHITECTURE.md § Module 008](ARCHITECTURE.md#module-008-mcp-server)

### Testing

- Running: [README.md § Running Tests](README.md#running-tests)
- Architecture: [ARCHITECTURE.md § Testing Architecture](ARCHITECTURE.md#testing-architecture)
- Spec: [0-docs/implementation steps/009-testing/](0-docs/implementation%20steps/009-testing/)

## 🆘 Troubleshooting

Common issues and solutions:

- [README.md § Troubleshooting](README.md#troubleshooting)
- [SETUP_GUIDE.md § Troubleshooting](SETUP_GUIDE.md#troubleshooting)

Quick fixes:

```bash
# Authentication issues
rm ~/.planner-cli/msal_cache.bin
python planner.py init-auth

# Configuration issues
cat ~/.planner-cli/config.json
chmod 600 ~/.planner-cli/config.json

# Permission issues
chmod +x planner.py
chmod 600 ~/.planner-cli/config.json
```

## 📊 Project Status

**Status:** ✅ Production Ready

- ✅ All 9 modules implemented
- ✅ 42+ test cases passing
- ✅ Complete documentation
- ✅ Zero linter errors
- ✅ Security best practices

See: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 🔗 External Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [Azure AD App Registration](https://portal.azure.com)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## 📝 Quick Reference

### CLI Commands

| Command | Description |
|---------|-------------|
| `init-auth` | Initialize authentication |
| `set-defaults` | Set default plan and bucket |
| `list-plans` | List available plans |
| `list-buckets` | List buckets in a plan |
| `add` | Create a new task |

### MCP Tools

| Tool | Description |
|------|-------------|
| `planner_initAuth` | Initialize authentication |
| `planner_createTask` | Create a task |
| `planner_setDefaults` | Set defaults |
| `planner_listPlans` | List plans |
| `planner_listBuckets` | List buckets |

### Configuration Files

| File | Purpose |
|------|---------|
| `~/.planner-cli/config.json` | User configuration |
| `~/.planner-cli/msal_cache.bin` | Token cache |
| Environment variables | Override config |

## 🤝 Contributing

This project follows a modular architecture. To contribute:

1. Review [ARCHITECTURE.md](ARCHITECTURE.md)
2. Check module specifications in `0-docs/implementation steps/`
3. Add tests for new features
4. Update documentation

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🎉 What's Next?

1. **Complete setup**: Follow [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **Try examples**: Review [EXAMPLES.md](EXAMPLES.md)
3. **Integrate with AI**: Set up MCP server (optional)
4. **Automate workflows**: Create shell scripts for common tasks

---

**Need help?** Start with [QUICKSTART.md](QUICKSTART.md) or check [README.md](README.md)
