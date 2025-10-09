# Setup Guide: Microsoft Planner Task Creator CLI + MCP Server

This guide walks you through the complete setup process from scratch.

> **💡 Don't have an Azure subscription?** You don't need one! Azure AD (Microsoft Entra ID) is free with Microsoft 365. See [SETUP_WITHOUT_AZURE_SUBSCRIPTION.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION.md) for detailed instructions on using:
> - Your work/school Microsoft 365 account
> - **Free Microsoft 365 Developer Program** (recommended for testing)
> - No Azure subscription required!

## 📚 Table of Contents

- [Prerequisites](prerequisites.md) - System requirements and dependencies
- [Azure AD Setup](azure-ad-setup.md) - App registration and permissions
- [CLI Installation](cli-installation.md) - Python CLI setup and configuration
- [Testing](testing.md) - Verify installation and functionality
- [MCP Server Setup](mcp-server-setup.md) - AI assistant integration (optional)
- [Verification](verification.md) - Test all components work together
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## 🎯 Quick Start

If you already have Azure AD set up, jump to:
- [CLI Installation](cli-installation.md) - Install and configure the CLI
- [Testing](testing.md) - Verify everything works

## 📋 Complete Setup Process

1. **Prerequisites** - Ensure system requirements are met
2. **Azure AD Setup** - Register app and configure permissions
3. **CLI Installation** - Install Python dependencies and configure
4. **Testing** - Verify CLI functionality
5. **MCP Server** - Optional AI assistant integration
6. **Verification** - End-to-end testing
7. **Troubleshooting** - Resolve any issues

## 🔧 Configuration Files

After setup, you'll have these configuration files:
- `~/.planner-cli/config.json` - CLI configuration
- `~/.planner-cli/msal_cache.bin` - Authentication token cache
- `~/.config/Cursor/mcp.json` - MCP server configuration (if using AI integration)
