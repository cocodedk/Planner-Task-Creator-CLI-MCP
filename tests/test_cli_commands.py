"""
Tests for CLI commands module (006-cli-commands)
"""

import pytest
import json
import sys
import os
from typer.testing import CliRunner

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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


def test_list_plans_success(mocker, mock_config_file, mock_plans):
    """Test listing plans"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client"
    })
    mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")
    mocker.patch("planner_lib.cli_commands.list_user_plans", return_value=mock_plans)

    result = runner.invoke(app, ["list-plans"])

    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert len(output) == 2
    assert output[0]["title"] == "My Plan"


def test_list_buckets_success(mocker, mock_config_file, mock_buckets):
    """Test listing buckets"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client"
    })
    mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")
    mocker.patch("planner_lib.cli_commands.resolve_plan", return_value={"id": "plan-id-1"})
    mocker.patch("planner_lib.cli_commands.list_plan_buckets", return_value=mock_buckets)

    result = runner.invoke(app, ["list-buckets", "--plan", "My Plan"])

    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert len(output) == 3
    assert output[0]["name"] == "To Do"


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
