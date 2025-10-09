"""
Tests for move_task_op function
"""

import pytest
import requests
from unittest.mock import Mock
from planner_lib.task_updates import move_task_op


@pytest.fixture
def mock_task_with_etag():
    """Return mock task with ETag"""
    return {
        "id": "task-id-123",
        "title": "Test Task",
        "percentComplete": 0,
        "@odata.etag": "W/\"abc123\""
    }


class TestMoveTask:
    """Tests for move_task_op function"""

    def test_move_task_success(self, mock_token, mock_task_with_etag, mocker):
        """Test successfully moving task to different bucket"""
        mock_get = mocker.patch("planner_lib.task_move.get_json")
        mock_get.return_value = mock_task_with_etag

        mock_patch = mocker.patch("planner_lib.task_move.patch_json")
        mock_patch.return_value = {"bucketId": "new-bucket-id"}

        result = move_task_op("task-id-123", "new-bucket-id", mock_token)

        assert result["bucketId"] == "new-bucket-id"
        mock_patch.assert_called_once()

    def test_move_task_etag_conflict_retry(self, mock_token, mock_task_with_etag, mocker):
        """Test ETag conflict with auto-retry"""
        mock_get = mocker.patch("planner_lib.task_move.get_json")
        mock_get.side_effect = [
            mock_task_with_etag,
            {**mock_task_with_etag, "@odata.etag": "W/\"new123\""}
        ]

        mock_patch = mocker.patch("planner_lib.task_move.patch_json")
        http_error = requests.HTTPError()
        http_error.response = Mock(status_code=412)
        mock_patch.side_effect = [http_error, {"bucketId": "new-bucket-id"}]

        result = move_task_op("task-id-123", "new-bucket-id", mock_token)

        assert result["bucketId"] == "new-bucket-id"
        assert mock_get.call_count == 2
