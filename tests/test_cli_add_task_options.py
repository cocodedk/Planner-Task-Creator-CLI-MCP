"""
CLI add task with options tests
"""

import json
from typer.testing import CliRunner
from planner import app

runner = CliRunner()


def test_add_task_with_all_options(mocker, mock_config_file):
    """Test adding task with all optional fields"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client",
        "default_plan": "My Plan", "default_bucket": "To Do"
    })
    mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")
    mocker.patch("planner_lib.cli_commands.resolve_plan", return_value={"id": "plan-id-1"})
    mocker.patch("planner_lib.cli_commands.resolve_bucket", return_value={"id": "bucket-id-1"})

    mock_create = mocker.patch("planner_lib.cli_commands.create_task", return_value={
        "taskId": "task-123",
        "webUrl": "https://planner.cloud.microsoft/tasks/task-123",
        "bucketId": "bucket-id-1"
    })

    result = runner.invoke(app, [
        "add",
        "--title", "Complete Task",
        "--desc", "Task description",
        "--due", "2024-12-31",
        "--labels", "Label1,Label2"
    ])

    assert result.exit_code == 0

    # Verify create_task was called with correct arguments
    mock_create.assert_called_once()
    call_kwargs = mock_create.call_args[1]
    assert call_kwargs["title"] == "Complete Task"
    assert call_kwargs["description"] == "Task description"
    assert call_kwargs["due_date"] == "2024-12-31"
    assert call_kwargs["labels"] == "Label1,Label2"


def test_add_task_verbose_output(mocker, mock_config_file):
    """Test verbose output for task creation"""
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

    result = runner.invoke(app, [
        "add",
        "--title", "Test Task",
        "--verbose"
    ])

    assert result.exit_code == 0
    assert "Task created" in result.stdout
    assert "task-123" in result.stdout


