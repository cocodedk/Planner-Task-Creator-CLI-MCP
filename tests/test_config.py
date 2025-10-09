"""
Tests for configuration management module (003-configuration)
"""

import pytest
import json
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from planner_lib.config import load_conf, save_conf, get_config_path


def test_load_conf_existing(mocker, mock_config_file):
    """Test loading existing configuration file"""
    mocker.patch("planner_lib.config.get_config_path", return_value=mock_config_file)

    cfg = load_conf()

    assert cfg["tenant_id"] == "test-tenant-id"
    assert cfg["client_id"] == "test-client-id"
    assert cfg["default_plan"] == "My Plan"
    assert cfg["default_bucket"] == "To Do"


def test_load_conf_nonexistent(mocker, tmp_path):
    """Test loading non-existent configuration file"""
    nonexistent_path = tmp_path / "nonexistent.json"
    mocker.patch("planner_lib.config.get_config_path", return_value=nonexistent_path)

    cfg = load_conf()

    assert cfg == {}


def test_save_conf(mocker, tmp_path):
    """Test saving configuration file"""
    config_path = tmp_path / ".planner-cli" / "config.json"
    mocker.patch("planner_lib.config.get_config_path", return_value=config_path)

    cfg = {
        "tenant_id": "new-tenant",
        "client_id": "new-client",
        "default_plan": "New Plan"
    }

    save_conf(cfg)

    # Verify file was created
    assert config_path.exists()

    # Verify content
    with open(config_path, 'r') as f:
        saved_cfg = json.load(f)

    assert saved_cfg == cfg

    # Verify permissions (on Unix systems)
    if os.name != 'nt':
        assert oct(config_path.stat().st_mode)[-3:] == '600'


def test_get_config_path_default():
    """Test default config path"""
    path = get_config_path()
    assert path.name == "config.json"
    assert ".planner-cli" in str(path)


def test_get_config_path_env(mocker):
    """Test config path from environment variable"""
    custom_path = "/custom/path/config.json"
    mocker.patch.dict(os.environ, {"PLANNER_CONFIG_PATH": custom_path})

    path = get_config_path()
    assert str(path) == custom_path


def test_save_conf_creates_directory(mocker, tmp_path):
    """Test that save_conf creates parent directory if needed"""
    config_path = tmp_path / "new_dir" / ".planner-cli" / "config.json"
    mocker.patch("planner_lib.config.get_config_path", return_value=config_path)

    cfg = {"tenant_id": "test"}
    save_conf(cfg)

    assert config_path.parent.exists()
    assert config_path.exists()
