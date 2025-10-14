"""
Tests for bucket_move module
"""

import pytest
from planner_lib.bucket_move import move_bucket_tasks_op


@pytest.fixture
def mock_tasks():
    """Return mock tasks data"""
    return [
        {"id": "task-id-1", "title": "Task 1", "bucketId": "source-bucket"},
        {"id": "task-id-2", "title": "Task 2", "bucketId": "source-bucket"},
        {"id": "task-id-3", "title": "Task 3", "bucketId": "source-bucket"}
    ]


class TestBucketMove:
    """Tests for move_bucket_tasks_op function"""

    def test_move_tasks_success(self, mock_token, mock_tasks, mocker):
        """Test moving all tasks from source to target bucket"""
        mock_get = mocker.patch("planner_lib.bucket_move.get_json")
        mock_move = mocker.patch("planner_lib.bucket_move.move_task_op")

        mock_get.return_value = {"value": mock_tasks}
        mock_move.return_value = {"ok": True}

        result = move_bucket_tasks_op("source-bucket", "target-bucket", mock_token)

        assert result["ok"] is True
        assert result["moved"] == 3
        assert result["failed"] == 0
        assert len(result["taskIds"]) == 3
        assert result["taskIds"] == ["task-id-1", "task-id-2", "task-id-3"]
        assert len(result["errors"]) == 0

        # Verify all tasks were moved
        assert mock_move.call_count == 3
        for i, task_id in enumerate(["task-id-1", "task-id-2", "task-id-3"]):
            assert mock_move.call_args_list[i][0][0] == task_id
            assert mock_move.call_args_list[i][0][1] == "target-bucket"

    def test_move_tasks_empty_bucket(self, mock_token, mocker):
        """Test moving tasks from empty bucket"""
        mock_get = mocker.patch("planner_lib.bucket_move.get_json")
        mock_move = mocker.patch("planner_lib.bucket_move.move_task_op")

        mock_get.return_value = {"value": []}

        result = move_bucket_tasks_op("empty-bucket", "target-bucket", mock_token)

        assert result["ok"] is True
        assert result["moved"] == 0
        assert result["failed"] == 0
        assert len(result["taskIds"]) == 0

        # Verify no move operations were attempted
        mock_move.assert_not_called()

    def test_move_tasks_partial_failure(self, mock_token, mock_tasks, mocker):
        """Test moving tasks with some failures"""
        mock_get = mocker.patch("planner_lib.bucket_move.get_json")
        mock_move = mocker.patch("planner_lib.bucket_move.move_task_op")

        mock_get.return_value = {"value": mock_tasks}

        # Second task fails to move
        mock_move.side_effect = [
            {"ok": True},
            Exception("Task locked"),
            {"ok": True}
        ]

        result = move_bucket_tasks_op("source-bucket", "target-bucket", mock_token)

        assert result["ok"] is True
        assert result["moved"] == 2
        assert result["failed"] == 1
        assert len(result["taskIds"]) == 2
        assert "task-id-1" in result["taskIds"]
        assert "task-id-3" in result["taskIds"]
        assert len(result["errors"]) == 1
        assert result["errors"][0]["taskId"] == "task-id-2"
        assert "Task locked" in result["errors"][0]["error"]

    def test_move_tasks_source_not_found(self, mock_token, mocker):
        """Test moving from non-existent source bucket"""
        mock_get = mocker.patch("planner_lib.bucket_move.get_json")
        mock_get.side_effect = Exception("Bucket not found")

        with pytest.raises(Exception) as exc_info:
            move_bucket_tasks_op("invalid-bucket", "target-bucket", mock_token)

        assert "Bucket not found" in str(exc_info.value)

    def test_move_tasks_all_fail(self, mock_token, mock_tasks, mocker):
        """Test scenario where all task moves fail"""
        mock_get = mocker.patch("planner_lib.bucket_move.get_json")
        mock_move = mocker.patch("planner_lib.bucket_move.move_task_op")

        mock_get.return_value = {"value": mock_tasks}
        mock_move.side_effect = Exception("Target bucket not found")

        result = move_bucket_tasks_op("source-bucket", "invalid-target", mock_token)

        assert result["ok"] is True
        assert result["moved"] == 0
        assert result["failed"] == 3
        assert len(result["taskIds"]) == 0
        assert len(result["errors"]) == 3
