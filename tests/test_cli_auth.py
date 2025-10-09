"""
Tests for CLI authentication commands
"""

import json
from typer.testing import CliRunner
from planner import app

runner = CliRunner()


def test_init_auth_success(mocker, mock_config_file):
    """Test successful authentication initialization"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client"
    })
    mock_get_tokens = mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")

    result = runner.invoke(app, ["init-auth"])

    assert result.exit_code == 0
    assert "Authentication successful" in result.stdout
    mock_get_tokens.assert_called_once()


def test_init_auth_missing_config(mocker, tmp_path):
    """Test authentication with missing config"""
    empty_config = tmp_path / "empty.json"
    empty_config.write_text("{}")
    mocker.patch("planner_lib.config.get_config_path", return_value=empty_config)

    result = runner.invoke(app, ["init-auth"])

    assert result.exit_code == 2
    output = json.loads(result.stdout.strip().split("\n")[0])
    assert output["code"] == "ConfigError"


