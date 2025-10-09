# Configuration Management Specification

**Functions**:
- `load_conf() -> dict`
- `save_conf(cfg: dict) -> None`
- Configuration value resolution logic

**load_conf Implementation**:
1. Determine config path from `PLANNER_CONFIG_PATH` env var or default to `~/.planner-cli/config.json`
2. If file exists, read and parse JSON
3. If file doesn't exist or parsing fails, return empty dict `{}`
4. Return parsed configuration dictionary

**save_conf Implementation**:
1. Determine config path from `PLANNER_CONFIG_PATH` env var or default to `~/.planner-cli/config.json`
2. Create directory path if it doesn't exist
3. Write configuration dict as formatted JSON (indent=2)
4. Set file permissions to 0o600 (owner read/write only)

**Configuration Resolution**:
For any configuration value, resolve in this order:
1. CLI flag value (if provided)
2. Environment variable (if set)
3. Config file value (if exists)
4. None (if not found anywhere)

**Required Configuration Values**:
- `tenant_id`: Required for authentication
- `client_id`: Required for authentication
- `default_plan`: Optional, for default plan resolution
- `default_bucket`: Optional, for default bucket resolution

**Error Handling**: File I/O errors should be handled gracefully with fallbacks to empty config.
