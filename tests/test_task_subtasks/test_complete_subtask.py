"""
Tests for complete_subtask function
"""

import json
import pytest
import requests
from unittest.mock import Mock
from planner_lib.task_subtasks import complete_subtask
from .fixtures import mock_task_details


class TestCompleteSubtask:
    """Tests for complete_subtask function"""

    def test_complete_subtask_success(self, mock_token, mock_task_details, mocker):
        """Test successfully completing a subtask"""
        mock_get = mocker.patch("planner_lib.task_subtask_complete.get_json")
        mock_get.return_value = mock_task_details

        mock_patch = mocker.patch("planner_lib.task_subtask_complete.patch_json")
        mock_patch.return_value = {}

        result = complete_subtask("task-id-123", "Write tests", mock_token)

        assert result["ok"] is True
        assert result["subtaskId"] == "subtask-id-1"
        mock_patch.assert_called_once()

    def test_complete_subtask_case_insensitive(self, mock_token, mock_task_details, mocker):
        """Test case-insensitive subtask matching"""
        mock_get = mocker.patch("planner_lib.task_subtask_complete.get_json")
        mock_get.return_value = mock_task_details

        mock_patch = mocker.patch("planner_lib.task_subtask_complete.patch_json")
        mock_patch.return_value = {}

        result = complete_subtask("task-id-123", "WRITE TESTS", mock_token)

        assert result["ok"] is True
        assert result["subtaskId"] == "subtask-id-1"

    def test_complete_subtask_not_found(self, mock_token, mock_task_details, mocker):
        """Test error when subtask not found"""
        mock_get = mocker.patch("planner_lib.task_subtask_complete.get_json")
        mock_get.return_value = mock_task_details

        with pytest.raises(ValueError) as exc_info:
            complete_subtask("task-id-123", "Nonexistent subtask", mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "SubtaskNotFound"

    def test_complete_subtask_etag_conflict_retry(self, mock_token, mock_task_details, mocker):
        """Test ETag conflict with auto-retry"""
        mock_get = mocker.patch("planner_lib.task_subtask_complete.get_json")
        mock_get.side_effect = [
            mock_task_details,
            {**mock_task_details, "@odata.etag": "W/\"retry_etag\""}
        ]

        mock_patch = mocker.patch("planner_lib.task_subtask_complete.patch_json")
        http_error = requests.HTTPError()
        http_error.response = Mock(status_code=412)
        mock_patch.side_effect = [http_error, {}]

        result = complete_subtask("task-id-123", "Write tests", mock_token)

        assert result["ok"] is True
        assert mock_get.call_count == 2
        assert mock_patch.call_count == 2
