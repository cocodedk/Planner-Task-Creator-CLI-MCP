"""
Configuration Management Module
"""

import os
import json
from pathlib import Path


def get_config_path() -> Path:
    """Get configuration file path from environment or default."""
    config_path = os.environ.get("PLANNER_CONFIG_PATH")
    if config_path:
        return Path(config_path).expanduser()
    return Path.home() / ".planner-cli" / "config.json"


def load_conf() -> dict:
    """Load configuration from file, return empty dict if not found."""
    config_path = get_config_path()
    try:
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_conf(cfg: dict) -> None:
    """Save configuration to file with proper permissions."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(cfg, f, indent=2)

    # Set file permissions to 0600 (owner read/write only)
    os.chmod(config_path, 0o600)

