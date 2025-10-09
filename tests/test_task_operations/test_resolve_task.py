"""
Tests for resolve_task function
"""

import json
import pytest
from planner_lib.task_operations import resolve_task


@pytest.fixture
def mock_tasks():
    """Return mock tasks data"""
    return [
        {
            "id": "task-id-1",
            "title": "Task One",
            "bucketId": "bucket-id-1",
            "planId": "plan-id-1",
            "percentComplete": 0
        },
        {
            "id": "task-id-2",
            "title": "Task Two",
            "bucketId": "bucket-id-1",
            "planId": "plan-id-1",
            "percentComplete": 50
        }
    ]


class TestResolveTask:
    """Tests for resolve_task function"""

    def test_resolve_task_by_guid(self, mock_token, mocker):
        """Test resolving task by GUID"""
        task_id = "12345678-1234-1234-1234-123456789012"
        mock_task = {"id": task_id, "title": "Test Task"}

        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.return_value = mock_task

        result = resolve_task(mock_token, task_id)

        assert result["id"] == task_id
        mock_get.assert_called_once()

    def test_resolve_task_by_title_exact_match(self, mock_token, mock_tasks, mocker):
        """Test resolving task by exact title match"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        result = resolve_task(mock_token, "Task One", plan_id="plan-id-1")

        assert result["title"] == "Task One"
        assert result["id"] == "task-id-1"

    def test_resolve_task_by_title_case_insensitive(self, mock_token, mock_tasks, mocker):
        """Test case-insensitive title matching"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        result = resolve_task(mock_token, "task one", plan_id="plan-id-1")

        assert result["title"] == "Task One"

    def test_resolve_task_ambiguous_title(self, mock_token, mocker):
        """Test error when multiple tasks match title"""
        ambiguous_tasks = [
            {"id": "task-id-1", "title": "Test", "bucketId": "bucket-1"},
            {"id": "task-id-2", "title": "Test", "bucketId": "bucket-2"}
        ]

        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = ambiguous_tasks

        with pytest.raises(ValueError) as exc_info:
            resolve_task(mock_token, "Test", plan_id="plan-id-1")

        error = json.loads(str(exc_info.value))
        assert error["code"] == "AmbiguousTask"
        assert len(error["candidates"]) == 2

    def test_resolve_task_not_found(self, mock_token, mock_tasks, mocker):
        """Test error when task not found"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        with pytest.raises(ValueError) as exc_info:
            resolve_task(mock_token, "Nonexistent Task", plan_id="plan-id-1")

        error = json.loads(str(exc_info.value))
        assert error["code"] == "TaskNotFound"

    def test_resolve_task_by_title_without_plan_raises_error(self, mock_token):
        """Test that title search without plan_id raises error"""
        with pytest.raises(ValueError) as exc_info:
            resolve_task(mock_token, "Some Task")

        error = json.loads(str(exc_info.value))
        assert error["code"] == "ConfigError"
