# Environment Setup Guide

This guide explains how to manage your Azure AD credentials securely.

## 📚 Table of Contents

- [Quick Answer](quick-answer.md) - Quick overview of credential management
- [Why Both Methods](why-both.md) - Understanding the dual approach
- [Setup Methods](setup-methods.md) - Three different credential management approaches
- [Security Best Practices](security-practices.md) - How to keep credentials secure
- [Files Overview](files-overview.md) - What files contain credentials and where
- [Method Selection](method-selection.md) - Which method to use when
- [Getting Credentials](getting-credentials.md) - How to obtain your Azure AD credentials
- [Updating Scripts](updating-scripts.md) - How to update existing setup scripts
- [Troubleshooting](troubleshooting.md) - Common credential issues and solutions
- [Summary](summary.md) - Key takeaways about credential management

## 🎯 Key Points

- **Cursor MCP:** Credentials in `~/.config/Cursor/mcp.json`
- **CLI Development:** `.env` file or environment variables
- **MCP Server:** Needs credentials passed through `mcp.json` env section
- **Security:** Never commit actual credentials to git

## 🔐 Security First

- ✅ Use `.env` for development (in `.gitignore`)
- ✅ Use `mcp.json` for Cursor (in home directory)
- ❌ Never commit `.env` files
- ❌ Never hardcode credentials
