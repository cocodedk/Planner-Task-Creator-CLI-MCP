"""
Tests for list_subtasks function
"""

import pytest
from planner_lib.task_subtasks import list_subtasks
from .fixtures import mock_task_details, mock_empty_task_details


class TestListSubtasks:
    """Tests for list_subtasks function"""

    def test_list_subtasks_with_items(self, mock_token, mock_task_details, mocker):
        """Test listing subtasks from task with checklist"""
        mock_get = mocker.patch("planner_lib.task_subtask_list.get_json")
        mock_get.return_value = mock_task_details

        result = list_subtasks("task-id-123", mock_token)

        assert len(result) == 2
        assert result[0]["id"] == "subtask-id-1"
        assert result[0]["title"] == "Write tests"
        assert result[0]["isChecked"] is False
        assert result[1]["isChecked"] is True

    def test_list_subtasks_empty_checklist(self, mock_token, mock_empty_task_details, mocker):
        """Test listing subtasks from task without checklist"""
        mock_get = mocker.patch("planner_lib.task_subtask_list.get_json")
        mock_get.return_value = mock_empty_task_details

        result = list_subtasks("task-id-456", mock_token)

        assert len(result) == 0
