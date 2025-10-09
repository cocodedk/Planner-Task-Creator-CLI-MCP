"""
Basic CLI add task tests
"""

import json
from typer.testing import CliRunner
from planner import app

runner = CliRunner()


def test_add_task_with_defaults(mocker, mock_config_file):
    """Test adding task with defaults from config"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client",
        "default_plan": "My Plan", "default_bucket": "To Do"
    })
    mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")
    mocker.patch("planner_lib.cli_commands.resolve_plan", return_value={"id": "plan-id-1"})
    mocker.patch("planner_lib.cli_commands.resolve_bucket", return_value={"id": "bucket-id-1"})
    mocker.patch("planner_lib.cli_commands.create_task", return_value={
        "taskId": "task-123",
        "webUrl": "https://planner.cloud.microsoft/tasks/task-123",
        "bucketId": "bucket-id-1"
    })

    result = runner.invoke(app, ["add", "--title", "Test Task"])

    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["taskId"] == "task-123"


def test_add_task_missing_plan_bucket(mocker, tmp_path):
    """Test adding task without plan/bucket specified"""
    empty_config = tmp_path / "config.json"
    empty_config.write_text(json.dumps({
        "tenant_id": "test-tenant",
        "client_id": "test-client"
    }))
    mocker.patch("planner_lib.config.get_config_path", return_value=empty_config)

    result = runner.invoke(app, ["add", "--title", "Test Task"])

    assert result.exit_code == 2
    output = json.loads(result.stdout.strip().split("\n")[0])
    assert output["code"] == "ConfigError"


