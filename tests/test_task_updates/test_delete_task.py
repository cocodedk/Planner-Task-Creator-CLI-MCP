"""
Tests for delete_task_op function
"""

import pytest
from unittest.mock import Mock
from planner_lib.task_updates import delete_task_op


@pytest.fixture
def mock_task_with_etag():
    """Return mock task with ETag"""
    return {
        "id": "task-id-123",
        "title": "Test Task",
        "percentComplete": 0,
        "@odata.etag": "W/\"abc123\""
    }


class TestDeleteTask:
    """Tests for delete_task_op function"""

    def test_delete_task_success(self, mock_token, mock_task_with_etag, mocker):
        """Test successfully deleting task"""
        mock_get = mocker.patch("planner_lib.task_delete.get_json")
        mock_get.return_value = mock_task_with_etag

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None

        mock_delete = mocker.patch("requests.delete")
        mock_delete.return_value = mock_response

        result = delete_task_op("task-id-123", mock_token)

        assert result["ok"] is True
        assert result["taskId"] == "task-id-123"
        mock_delete.assert_called_once()

    def test_delete_task_includes_etag(self, mock_token, mock_task_with_etag, mocker):
        """Test that delete request includes ETag header"""
        mock_get = mocker.patch("planner_lib.task_delete.get_json")
        mock_get.return_value = mock_task_with_etag

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None

        mock_delete = mocker.patch("requests.delete")
        mock_delete.return_value = mock_response

        delete_task_op("task-id-123", mock_token)

        # Verify ETag was included in headers
        call_args = mock_delete.call_args
        headers = call_args[1]["headers"]
        assert "If-Match" in headers
        assert headers["If-Match"] == "W/\"abc123\""
