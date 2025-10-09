"""
Tests for complete_task_op function
"""

import pytest
import requests
from unittest.mock import Mock
from planner_lib.task_updates import complete_task_op


@pytest.fixture
def mock_task_with_etag():
    """Return mock task with ETag"""
    return {
        "id": "task-id-123",
        "title": "Test Task",
        "percentComplete": 0,
        "@odata.etag": "W/\"abc123\""
    }


class TestCompleteTask:
    """Tests for complete_task_op function"""

    def test_complete_task_success(self, mock_token, mock_task_with_etag, mocker):
        """Test successfully marking task as complete"""
        mock_get = mocker.patch("planner_lib.task_complete.get_json")
        mock_get.return_value = mock_task_with_etag

        mock_patch = mocker.patch("planner_lib.task_complete.patch_json")
        mock_patch.return_value = {"percentComplete": 100}

        result = complete_task_op("task-id-123", mock_token)

        assert result["percentComplete"] == 100
        mock_patch.assert_called_once()

    def test_complete_task_etag_conflict_retry(self, mock_token, mock_task_with_etag, mocker):
        """Test ETag conflict with auto-retry"""
        mock_get = mocker.patch("planner_lib.task_complete.get_json")
        mock_get.side_effect = [
            mock_task_with_etag,  # First fetch
            {**mock_task_with_etag, "@odata.etag": "W/\"def456\""}  # Retry fetch
        ]

        mock_patch = mocker.patch("planner_lib.task_complete.patch_json")
        # First call raises 412, second succeeds
        http_error = requests.HTTPError()
        http_error.response = Mock(status_code=412)
        mock_patch.side_effect = [http_error, {"percentComplete": 100}]

        result = complete_task_op("task-id-123", mock_token)

        assert result["percentComplete"] == 100
        assert mock_get.call_count == 2
        assert mock_patch.call_count == 2
