# Configuration Management Context

**Purpose**: Handle config file loading, saving, and defaults resolution for CLI.

**Scope**: Manage `~/.planner-cli/config.json` with secure file permissions.

**Key Requirements**:
- Load config with fallback to empty dict
- Save config with proper JSON formatting and permissions
- Resolve configuration values from multiple sources (CLI flags, env vars, config file)
- Secure file permissions (0600)
