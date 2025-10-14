"""
CLI Integration Tests for Bucket Operations
"""

import json
import pytest
from typer.testing import CliRunner
from planner import app

runner = CliRunner()


@pytest.fixture
def mock_bucket_env(mocker):
    """Mock environment and dependencies for bucket operations"""
    # Mock config
    mock_config = {
        "tenant_id": "test-tenant-id",
        "client_id": "test-client-id"
    }
    mocker.patch("planner_lib.cli_bucket_commands.load_conf", return_value=mock_config)

    # Mock auth
    mocker.patch("planner_lib.cli_bucket_commands.get_tokens", return_value="mock-token")

    # Mock resolution
    mock_plan = {"id": "plan-123", "name": "Test Plan"}
    mock_bucket = {"id": "bucket-123", "name": "Test Bucket"}
    mocker.patch("planner_lib.cli_bucket_commands.resolve_plan", return_value=mock_plan)
    mocker.patch("planner_lib.cli_bucket_commands.resolve_bucket", return_value=mock_bucket)

    return {
        "plan": mock_plan,
        "bucket": mock_bucket
    }


class TestCreateBucketCLI:
    """Tests for create-bucket CLI command"""

    def test_create_bucket_success(self, mock_bucket_env, mocker):
        """Test successful bucket creation via CLI"""
        mock_create = mocker.patch("planner_lib.cli_bucket_commands.create_bucket_op")
        mock_create.return_value = {
            "ok": True,
            "bucketId": "new-bucket-123",
            "name": "Sprint 1",
            "planId": "plan-123"
        }

        result = runner.invoke(app, [
            "create-bucket",
            "--name", "Sprint 1",
            "--plan", "Test Plan"
        ])

        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert output["ok"] is True
        assert output["bucketId"] == "new-bucket-123"
        assert output["name"] == "Sprint 1"

    def test_create_bucket_missing_name(self):
        """Test error when name is missing"""
        result = runner.invoke(app, [
            "create-bucket",
            "--plan", "Test Plan"
        ])

        assert result.exit_code != 0

    def test_create_bucket_missing_plan(self):
        """Test error when plan is missing"""
        result = runner.invoke(app, [
            "create-bucket",
            "--name", "Sprint 1"
        ])

        assert result.exit_code != 0


class TestDeleteBucketCLI:
    """Tests for delete-bucket CLI command"""

    def test_delete_bucket_success(self, mock_bucket_env, mocker):
        """Test successful bucket deletion via CLI"""
        mock_delete = mocker.patch("planner_lib.cli_bucket_commands.delete_bucket_op")
        mock_delete.return_value = {
            "ok": True,
            "bucketId": "bucket-123"
        }

        result = runner.invoke(app, [
            "delete-bucket",
            "--bucket", "Test Bucket",
            "--plan", "Test Plan"
        ])

        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert output["ok"] is True
        assert output["bucketId"] == "bucket-123"

    def test_delete_bucket_not_found(self, mock_bucket_env, mocker):
        """Test error when bucket not found"""
        error_json = json.dumps({
            "code": "NotFound",
            "message": "Bucket 'Invalid' not found"
        })
        mocker.patch("planner_lib.cli_bucket_commands.resolve_bucket", side_effect=ValueError(error_json))

        result = runner.invoke(app, [
            "delete-bucket",
            "--bucket", "Invalid",
            "--plan", "Test Plan"
        ])

        assert result.exit_code == 2
        output = json.loads(result.stdout)
        assert output["code"] == "NotFound"


class TestRenameBucketCLI:
    """Tests for rename-bucket CLI command"""

    def test_rename_bucket_success(self, mock_bucket_env, mocker):
        """Test successful bucket renaming via CLI"""
        mock_update = mocker.patch("planner_lib.cli_bucket_commands.update_bucket_op")
        mock_update.return_value = {
            "ok": True,
            "bucketId": "bucket-123",
            "oldName": "Sprint 1",
            "newName": "Sprint 1 - Complete"
        }

        result = runner.invoke(app, [
            "rename-bucket",
            "--bucket", "Sprint 1",
            "--new-name", "Sprint 1 - Complete",
            "--plan", "Test Plan"
        ])

        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert output["ok"] is True
        assert output["oldName"] == "Sprint 1"
        assert output["newName"] == "Sprint 1 - Complete"

    def test_rename_bucket_missing_new_name(self):
        """Test error when new name is missing"""
        result = runner.invoke(app, [
            "rename-bucket",
            "--bucket", "Sprint 1",
            "--plan", "Test Plan"
        ])

        assert result.exit_code != 0


class TestMoveBucketTasksCLI:
    """Tests for move-bucket-tasks CLI command"""

    def test_move_tasks_success(self, mock_bucket_env, mocker):
        """Test successful task movement via CLI"""
        # Mock source and target buckets
        source_bucket = {"id": "source-123", "name": "Source"}
        target_bucket = {"id": "target-456", "name": "Target"}

        resolve_mock = mocker.patch("planner_lib.cli_bucket_commands.resolve_bucket")
        resolve_mock.side_effect = [source_bucket, target_bucket]

        mock_move = mocker.patch("planner_lib.cli_bucket_commands.move_bucket_tasks_op")
        mock_move.return_value = {
            "ok": True,
            "moved": 5,
            "failed": 0,
            "taskIds": ["task-1", "task-2", "task-3", "task-4", "task-5"],
            "errors": []
        }

        result = runner.invoke(app, [
            "move-bucket-tasks",
            "--source", "Source",
            "--target", "Target",
            "--plan", "Test Plan"
        ])

        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert output["ok"] is True
        assert output["moved"] == 5
        assert output["failed"] == 0

    def test_move_tasks_partial_failure(self, mock_bucket_env, mocker):
        """Test task movement with some failures"""
        source_bucket = {"id": "source-123", "name": "Source"}
        target_bucket = {"id": "target-456", "name": "Target"}

        resolve_mock = mocker.patch("planner_lib.cli_bucket_commands.resolve_bucket")
        resolve_mock.side_effect = [source_bucket, target_bucket]

        mock_move = mocker.patch("planner_lib.cli_bucket_commands.move_bucket_tasks_op")
        mock_move.return_value = {
            "ok": True,
            "moved": 3,
            "failed": 2,
            "taskIds": ["task-1", "task-2", "task-3"],
            "errors": [
                {"taskId": "task-4", "error": "Task locked"},
                {"taskId": "task-5", "error": "Permission denied"}
            ]
        }

        result = runner.invoke(app, [
            "move-bucket-tasks",
            "--source", "Source",
            "--target", "Target",
            "--plan", "Test Plan"
        ])

        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert output["moved"] == 3
        assert output["failed"] == 2
        assert len(output["errors"]) == 2
