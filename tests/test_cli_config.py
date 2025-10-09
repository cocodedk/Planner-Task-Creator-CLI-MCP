"""
Tests for CLI configuration commands
"""

import json
from typer.testing import CliRunner
from planner import app

runner = CliRunner()


def test_set_defaults(mocker, tmp_path):
    """Test setting default plan and bucket"""
    config_path = tmp_path / "config.json"
    config_path.write_text("{}")
    mocker.patch("planner_lib.config.get_config_path", return_value=config_path)

    result = runner.invoke(app, [
        "set-defaults",
        "--plan", "My Plan",
        "--bucket", "To Do"
    ])

    assert result.exit_code == 0
    assert "Defaults saved" in result.stdout

    # Verify config was updated
    with open(config_path, 'r') as f:
        cfg = json.load(f)
    assert cfg["default_plan"] == "My Plan"
    assert cfg["default_bucket"] == "To Do"


