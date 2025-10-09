"""
Tests for add_subtask function
"""

import pytest
import requests
from unittest.mock import Mock
from planner_lib.task_subtasks import add_subtask
from .fixtures import mock_task_details, mock_empty_task_details


class TestAddSubtask:
    """Tests for add_subtask function"""

    def test_add_subtask_to_existing_checklist(self, mock_token, mock_task_details, mocker):
        """Test adding subtask to task with existing checklist"""
        mock_get = mocker.patch("planner_lib.task_subtask_add.get_json")
        mock_get.return_value = mock_task_details

        mock_patch = mocker.patch("planner_lib.task_subtask_add.patch_json")
        mock_patch.return_value = {}

        mocker.patch("uuid.uuid4", return_value="new-subtask-id")

        result = add_subtask("task-id-123", "New subtask", mock_token)

        assert result["ok"] is True
        assert result["subtaskId"] == "new-subtask-id"
        mock_patch.assert_called_once()

    def test_add_subtask_to_empty_checklist(self, mock_token, mock_empty_task_details, mocker):
        """Test adding subtask to task without checklist"""
        mock_get = mocker.patch("planner_lib.task_subtask_add.get_json")
        mock_get.return_value = mock_empty_task_details

        mock_patch = mocker.patch("planner_lib.task_subtask_add.patch_json")
        mock_patch.return_value = {}

        mocker.patch("uuid.uuid4", return_value="first-subtask-id")

        result = add_subtask("task-id-456", "First subtask", mock_token)

        assert result["ok"] is True
        assert result["subtaskId"] == "first-subtask-id"

    def test_add_subtask_etag_conflict_retry(self, mock_token, mock_task_details, mocker):
        """Test ETag conflict with auto-retry"""
        mock_get = mocker.patch("planner_lib.task_subtask_add.get_json")
        mock_get.side_effect = [
            mock_task_details,
            {**mock_task_details, "@odata.etag": "W/\"new_etag\""}
        ]

        mock_patch = mocker.patch("planner_lib.task_subtask_add.patch_json")
        http_error = requests.HTTPError()
        http_error.response = Mock(status_code=412)
        mock_patch.side_effect = [http_error, {}]

        mocker.patch("uuid.uuid4", return_value="retry-subtask-id")

        result = add_subtask("task-id-123", "Retry subtask", mock_token)

        assert result["ok"] is True
        assert mock_get.call_count == 2
        assert mock_patch.call_count == 2
