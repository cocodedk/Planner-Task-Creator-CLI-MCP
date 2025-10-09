"""
CLI add task error handling tests
"""

import json
from typer.testing import CliRunner
from planner import app

runner = CliRunner()


def test_add_task_resolution_error(mocker, mock_config_file):
    """Test adding task with plan resolution error"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client",
        "default_plan": "My Plan", "default_bucket": "To Do"
    })
    mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")

    error_json = json.dumps({
        "code": "NotFound",
        "message": "Plan not found",
        "candidates": []
    })
    mocker.patch("planner_lib.cli_commands.resolve_plan", side_effect=ValueError(error_json))

    result = runner.invoke(app, ["add", "--title", "Test Task"])

    assert result.exit_code == 2
    output = json.loads(result.stdout.strip().split("\n")[0])
    assert output["code"] == "NotFound"


