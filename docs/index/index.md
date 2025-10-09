# Documentation Index

Welcome to the Microsoft Planner Task Creator CLI + MCP Server documentation!

## 🚀 Getting Started

Start here if you're new to the project:

### Core Documentation
- **[SETUP_GUIDE/](SETUP_GUIDE/SETUP_GUIDE.md)** - Complete setup instructions including Azure AD configuration
- **[SETUP_WITHOUT_AZURE_SUBSCRIPTION/](SETUP_WITHOUT_AZURE_SUBSCRIPTION/SETUP_WITHOUT_AZURE_SUBSCRIPTION.md)** - ⭐ **No Azure subscription? Start here!**
- **[ARCHITECTURE/](ARCHITECTURE/ARCHITECTURE.md)** - Technical architecture and design decisions
- **[TEST_RESULTS/](TEST_RESULTS/TEST_RESULTS.md)** - Test suite results and status

### Quick Start Guides
- **[QUICKSTART.md](../QUICKSTART.md)** - 5-minute quick start guide for the Python CLI
- **[README.md](../README.md)** - Main documentation with full feature list and usage
- **[EXAMPLES.md](../EXAMPLES.md)** - Practical examples and real-world workflows

### Technical Documentation
- **[ARCHITECTURE/](ARCHITECTURE/ARCHITECTURE.md)** - System architecture and design
- **[PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md)** - Implementation summary and status

### Reference
- **[0-docs/prd.md](../0-docs/prd.md)** - Product requirements document
- **[0-docs/implementation steps/](../0-docs/implementation%20steps/)** - Detailed module specifications

## 🎯 Quick Links

### Installation
```bash
# Quick install
./scripts/INSTALLATION.sh

# Or manual install
pip install -r requirements.txt
cp planner.py ~/.planner-cli/
```

See: [SETUP_GUIDE/](SETUP_GUIDE/SETUP_GUIDE.md)

### First Steps
```bash
# 1. Authenticate
python planner.py init-auth

# 2. Set defaults
python planner.py set-defaults --plan "My Plan" --bucket "To Do"

# 3. Create task
python planner.py add --title "My first task"
```

See: [SETUP_GUIDE/](SETUP_GUIDE/SETUP_GUIDE.md)

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

See: [EXAMPLES.md](../EXAMPLES.md)

## 📂 Project Structure

```
planner-task-creator-cli-mcp/
├── planner.py              # Main Python CLI
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
├── scripts/               # Shell scripts
│   └── INSTALLATION.sh    # Automated installer
├── src/
│   └── server.ts         # MCP server
│
├── tests/
│   ├── __init__.py       # Test fixtures
│   ├── test_auth.py      # Auth tests
│   ├── test_config.py    # Config tests
│   ├── test_resolution.py
│   ├── test_task_creation.py
│   └── test_cli_commands.py
│
├── 0-docs/
│   ├── prd.md            # Product requirements
│   └── implementation steps/ # Detailed specifications
│       ├── 000-overview.md
│       ├── 001-authentication/
│       ├── 002-graph-client/
│       └── ... (9 modules total)
│
└── Documentation/
    ├── index/            # This index (refactored)
    ├── ARCHITECTURE/     # Architecture docs (refactored)
    ├── SETUP_GUIDE/      # Setup guide (refactored)
    ├── SETUP_WITHOUT_AZURE_SUBSCRIPTION/ # No subscription guide (refactored)
    ├── TEST_RESULTS/     # Test results (refactored)
    ├── README.md         # Main docs
    ├── QUICKSTART.md     # Quick start
    ├── EXAMPLES.md       # Examples
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

See: [ARCHITECTURE/](ARCHITECTURE/ARCHITECTURE.md)

## 📚 Documentation by Topic

### Authentication
- Setup: [SETUP_GUIDE/azure-ad-setup.md](SETUP_GUIDE/azure-ad-setup.md)
- Usage: [README.md](../README.md#initialize-authentication)
- Architecture: [ARCHITECTURE/modules.md](ARCHITECTURE/modules.md#module-001-authentication)
- Spec: [../0-docs/implementation steps/001-authentication/](../0-docs/implementation%20steps/001-authentication/)

### Configuration
- Setup: [SETUP_GUIDE/cli-installation.md](SETUP_GUIDE/cli-installation.md)
- Usage: [README.md](../README.md#configuration)
- Examples: [EXAMPLES.md](../EXAMPLES.md#configuration)
- Architecture: [ARCHITECTURE/modules.md](ARCHITECTURE/modules.md#module-003-configuration-management)

### Task Creation
- Usage: [README.md](../README.md#create-a-task)
- Examples: [EXAMPLES.md](../EXAMPLES.md#task-creation)
- Architecture: [ARCHITECTURE/modules.md](ARCHITECTURE/modules.md#module-005-task-creation)
- Spec: [../0-docs/implementation steps/005-task-creation/](../0-docs/implementation%20steps/005-task-creation/)

### Task Assignment
- Setup: [SETUP_GUIDE/azure-ad-setup.md](SETUP_GUIDE/azure-ad-setup.md)
- Requirements: [TEST_RESULTS/task-assignment-permissions.md](TEST_RESULTS/task-assignment-permissions.md)
- Architecture: [ARCHITECTURE/task-assignment.md](ARCHITECTURE/task-assignment.md)
- Spec: [../0-docs/implementation steps/012-task-assignment/](../0-docs/implementation%20steps/012-task-assignment/)

### MCP Server
- Setup: [SETUP_GUIDE/mcp-server-setup.md](SETUP_GUIDE/mcp-server-setup.md)
- Usage: [README.md](../README.md#mcp-server)
- Examples: [EXAMPLES.md](../EXAMPLES.md#mcp-server-usage)
- Architecture: [ARCHITECTURE/modules.md](ARCHITECTURE/modules.md#module-008-mcp-server)

### Testing
- Running: [README.md](../README.md#running-tests)
- Architecture: [ARCHITECTURE/testing.md](ARCHITECTURE/testing.md)
- Results: [TEST_RESULTS/TEST_RESULTS.md](TEST_RESULTS/TEST_RESULTS.md)
- Spec: [../0-docs/implementation steps/009-testing/](../0-docs/implementation%20steps/009-testing/)

## 🆘 Troubleshooting

Common issues and solutions:
- [SETUP_GUIDE/troubleshooting.md](SETUP_GUIDE/troubleshooting.md)
- [SETUP_WITHOUT_AZURE_SUBSCRIPTION/faq.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION/faq.md)

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

See: [TEST_RESULTS/TEST_RESULTS.md](TEST_RESULTS/TEST_RESULTS.md)

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

1. Review [ARCHITECTURE/](ARCHITECTURE/ARCHITECTURE.md)
2. Check module specifications in `../0-docs/implementation steps/`
3. Add tests for new features
4. Update documentation

## 📄 License

MIT License - see [LICENSE](../LICENSE)

## 🎉 What's Next?

1. **Complete setup**: Follow [SETUP_GUIDE/](SETUP_GUIDE/SETUP_GUIDE.md)
2. **Try examples**: Review [EXAMPLES.md](../EXAMPLES.md)
3. **Integrate with AI**: Set up MCP server (optional)
4. **Automate workflows**: Create shell scripts for common tasks

---

**Need help?** Start with [SETUP_GUIDE/](SETUP_GUIDE/SETUP_GUIDE.md) or check [README.md](../README.md)
