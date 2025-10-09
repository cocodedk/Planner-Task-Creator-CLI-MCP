# Setting Up Planner MCP Server in Cursor

This guide shows you how to add the Microsoft Planner MCP server to Cursor editor.

## 📚 Table of Contents

- [Prerequisites](prerequisites.md) - Requirements before starting
- [Configuration Location](configuration-location.md) - Where to find config files by OS
- [Configuration Setup](configuration-setup.md) - Creating and editing the config file
- [Virtual Environment](virtual-environment.md) - Setting up Python virtual environment
- [Restart Cursor](restart-cursor.md) - Restarting Cursor to load the server
- [Verification](verification.md) - Testing that everything works
- [MCP Tools](mcp-tools.md) - Available tools reference
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Setup Script](setup-script.md) - Automated setup script
- [Testing](testing.md) - Testing without Cursor
- [Summary](summary.md) - What you get after setup

## 🎯 Quick Setup

1. **Locate config file** based on your OS
2. **Create/edit** `mcp.json` with server configuration
3. **Restart Cursor** completely
4. **Test** by asking "Can you list my Planner plans?"

## 🚀 Integration Features

After setup, Cursor AI can:
- ✅ Create tasks through natural language
- ✅ List plans and buckets
- ✅ Set defaults and manage tasks
- ✅ Use existing authentication tokens

## 🔧 Configuration Required

You'll need to configure:
- **Server path:** Absolute path to `dist/server.js`
- **CLI path:** Absolute path to `planner.py`
- **Credentials:** TENANT_ID and CLIENT_ID
- **Defaults:** Optional default plan and bucket
