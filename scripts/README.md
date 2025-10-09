# Scripts

This directory contains shell scripts for setup, testing, and automation.

## 📜 Available Scripts

### Installation & Setup

#### `INSTALLATION.sh`
Automated installation script for the complete project setup.

**Usage:**
```bash
./scripts/INSTALLATION.sh
```

**What it does:**
- Checks Python 3.8+ installation
- Checks Node.js 18+ installation (optional)
- Creates Python virtual environment
- Installs Python dependencies
- Installs Node.js dependencies
- Builds TypeScript MCP server
- Displays next steps

---

#### `setup-cursor-mcp.sh`
Configures Cursor IDE to use the MCP server.

**Usage:**
```bash
./scripts/setup-cursor-mcp.sh
```

**What it does:**
- Creates or updates `~/.config/Cursor/mcp.json`
- Configures environment variables
- Sets up server command with absolute paths
- Provides restart instructions

**Requirements:**
- Edit the script to set your `PROJECT_DIR` and credentials
- Run from project root directory

---

### Testing

#### `QUICKTEST.sh`
Quick test of the Python CLI functionality.

**Usage:**
```bash
./scripts/QUICKTEST.sh
```

**What it does:**
- Activates Python virtual environment
- Runs basic CLI commands
- Tests authentication and configuration

---

#### `test-mcp-server.sh`
Tests the MCP server functionality.

**Usage:**
```bash
./scripts/test-mcp-server.sh
```

**What it does:**
- Tests MCP server initialization
- Validates tool definitions
- Checks server responses

---

## 🔧 Script Maintenance

All scripts are designed to be:
- **Executable:** Run `chmod +x scripts/*.sh` if needed
- **Portable:** Work from project root directory
- **Fail-safe:** Exit on errors with clear messages
- **Colored output:** Use green/red/yellow for better readability

## 📝 Notes

- Scripts should be run from the project root directory
- Some scripts require configuration (see script comments)
- All scripts use `/bin/bash` shebang
- Scripts assume Unix-like environment (Linux/macOS)

