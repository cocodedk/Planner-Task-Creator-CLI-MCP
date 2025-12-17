# Scripts

This directory contains scripts for setup, testing, and automation.

## 📜 Available Scripts

### Installation & Setup

#### `INSTALLATION.sh` (Linux/macOS)
Automated installation script for the complete project setup on Unix-like systems.

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

#### `INSTALLATION.ps1` (Windows PowerShell)
Automated installation script for Windows using PowerShell.

**Usage:**
```powershell
# You may need to allow script execution first:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Run the installation
.\scripts\INSTALLATION.ps1
```

**What it does:**
- Checks Python 3.8+ installation
- Checks Node.js 18+ installation (optional)
- Creates Python virtual environment in project directory
- Installs Python dependencies
- Copies CLI to `%USERPROFILE%\.planner-cli`
- Optionally installs and builds MCP server
- Guides through Azure AD configuration

---

#### `INSTALLATION.bat` (Windows Command Prompt)
Automated installation script for Windows using Command Prompt (batch file).

**Usage:**
```cmd
scripts\INSTALLATION.bat
```

**What it does:**
- Same functionality as the PowerShell version
- Works without PowerShell execution policy changes
- Compatible with older Windows systems

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
- **Executable:** Run `chmod +x scripts/*.sh` if needed (Unix)
- **Portable:** Work from project root directory
- **Fail-safe:** Exit on errors with clear messages
- **Colored output:** Use green/red/yellow for better readability

## 📝 Notes

- Scripts should be run from the project root directory
- Some scripts require configuration (see script comments)

### Platform-Specific Notes

**Linux/macOS:**
- Shell scripts use `/bin/bash` shebang
- Run `chmod +x scripts/*.sh` to make scripts executable

**Windows:**
- Use `INSTALLATION.ps1` for PowerShell (recommended)
- Use `INSTALLATION.bat` for Command Prompt
- You may need to set PowerShell execution policy:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
- Virtual environment activation: `venv\Scripts\activate.bat` or `.\venv\Scripts\Activate.ps1`
