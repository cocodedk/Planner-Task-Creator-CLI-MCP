"""
Tests for get_task_details and find_task_by_title functions
"""

import json
import pytest
from planner_lib.task_operations import get_task_details, find_task_by_title


@pytest.fixture
def mock_task_id():
    """Valid GUID for testing"""
    return "8bc07d47-c06f-459f-b97e-49c4d6a1b042"


@pytest.fixture
def mock_task(mock_task_id):
    """Return mock task data"""
    return {
        "id": mock_task_id,
        "title": "Test Task",
        "bucketId": "bucket-123",
        "planId": "plan-123",
        "percentComplete": 0
    }


@pytest.fixture
def mock_tasks():
    """Return mock tasks list"""
    return [
        {
            "id": "task-id-1",
            "title": "Fix Login Bug",
            "bucketId": "bucket-1",
            "percentComplete": 0
        },
        {
            "id": "task-id-2",
            "title": "Update Documentation",
            "bucketId": "bucket-1",
            "percentComplete": 50
        },
        {
            "id": "task-id-3",
            "title": "Fix API Bug",
            "bucketId": "bucket-2",
            "percentComplete": 0
        }
    ]


class TestGetTaskDetails:
    """Tests for get_task_details function"""

    def test_get_task_details_valid_id(self, mock_token, mock_task_id, mock_task, mocker):
        """Test fetching task details with valid GUID"""
        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.return_value = mock_task

        result = get_task_details(mock_task_id, mock_token)

        assert result["id"] == mock_task_id
        assert result["title"] == "Test Task"
        mock_get.assert_called_once()

    def test_get_task_details_invalid_format_short(self, mock_token):
        """Test error with invalid GUID format (too short)"""
        invalid_id = "not-a-guid"

        with pytest.raises(ValueError) as exc_info:
            get_task_details(invalid_id, mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "InvalidTaskId"
        assert "Invalid task ID format" in error["message"]

    def test_get_task_details_invalid_format_empty(self, mock_token):
        """Test error with empty task ID"""
        with pytest.raises(ValueError) as exc_info:
            get_task_details("", mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "InvalidTaskId"

    def test_get_task_details_invalid_format_random_string(self, mock_token):
        """Test error with random string"""
        invalid_id = "just-some-text"

        with pytest.raises(ValueError) as exc_info:
            get_task_details(invalid_id, mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "InvalidTaskId"

    def test_get_task_details_not_found(self, mock_token, mock_task_id, mocker):
        """Test error when task not found (404)"""
        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.side_effect = ValueError(json.dumps({
            "code": "NotFound",
            "message": "Task not found"
        }))

        with pytest.raises(ValueError) as exc_info:
            get_task_details(mock_task_id, mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "NotFound"

    def test_get_task_details_correct_url(self, mock_token, mock_task_id, mock_task, mocker):
        """Test that correct Graph API URL is called"""
        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.return_value = mock_task

        get_task_details(mock_task_id, mock_token)

        call_args = mock_get.call_args
        url = call_args[0][0]
        assert f"/planner/tasks/{mock_task_id}" in url


class TestFindTaskByTitle:
    """Tests for find_task_by_title function"""

    def test_find_task_by_title_single_match(self, mock_token, mock_tasks, mocker):
        """Test finding task with single exact match"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        result = find_task_by_title("Update Documentation", "plan-123", mock_token)

        assert result["title"] == "Update Documentation"
        assert result["id"] == "task-id-2"

    def test_find_task_by_title_case_insensitive(self, mock_token, mock_tasks, mocker):
        """Test case-insensitive title matching"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        result = find_task_by_title("fix login bug", "plan-123", mock_token)

        assert result["title"] == "Fix Login Bug"
        assert result["id"] == "task-id-1"

    def test_find_task_by_title_mixed_case(self, mock_token, mock_tasks, mocker):
        """Test mixed case matching"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        result = find_task_by_title("UPDATE documentation", "plan-123", mock_token)

        assert result["title"] == "Update Documentation"

    def test_find_task_by_title_ambiguous(self, mock_token, mocker):
        """Test error when multiple tasks match"""
        ambiguous_tasks = [
            {"id": "task-1", "title": "Fix Bug", "bucketId": "bucket-1"},
            {"id": "task-2", "title": "Fix Bug", "bucketId": "bucket-2"}
        ]

        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = ambiguous_tasks

        with pytest.raises(ValueError) as exc_info:
            find_task_by_title("Fix Bug", "plan-123", mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "AmbiguousTask"
        assert len(error["candidates"]) == 2
        assert "Multiple tasks match" in error["message"]

    def test_find_task_by_title_not_found(self, mock_token, mock_tasks, mocker):
        """Test error when task not found"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        with pytest.raises(ValueError) as exc_info:
            find_task_by_title("Nonexistent Task", "plan-123", mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "TaskNotFound"
        assert "not found" in error["message"]
        assert "candidates" in error

    def test_find_task_by_title_candidates_in_error(self, mock_token, mock_tasks, mocker):
        """Test that error includes candidate suggestions"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        with pytest.raises(ValueError) as exc_info:
            find_task_by_title("Wrong Task", "plan-123", mock_token)

        error = json.loads(str(exc_info.value))
        assert "candidates" in error
        assert len(error["candidates"]) <= 5  # Max 5 candidates

    def test_find_task_by_title_calls_list_tasks(self, mock_token, mock_tasks, mocker):
        """Test that list_tasks is called with correct parameters"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        find_task_by_title("Fix Login Bug", "plan-123", mock_token)

        mock_list.assert_called_once_with(mock_token, plan_id="plan-123")

    def test_find_task_by_title_empty_string(self, mock_token, mock_tasks, mocker):
        """Test behavior with empty title string"""
        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        with pytest.raises(ValueError) as exc_info:
            find_task_by_title("", "plan-123", mock_token)

        error = json.loads(str(exc_info.value))
        assert error["code"] == "TaskNotFound"

    def test_find_task_by_title_special_characters(self, mock_token, mocker):
        """Test title with special characters"""
        tasks_with_special = [
            {"id": "task-1", "title": "Fix [Bug] #123", "bucketId": "bucket-1"}
        ]

        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = tasks_with_special

        result = find_task_by_title("Fix [Bug] #123", "plan-123", mock_token)

        assert result["title"] == "Fix [Bug] #123"

    def test_find_task_by_title_unicode(self, mock_token, mocker):
        """Test title with unicode characters"""
        tasks_with_unicode = [
            {"id": "task-1", "title": "修复错误", "bucketId": "bucket-1"}
        ]

        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = tasks_with_unicode

        result = find_task_by_title("修复错误", "plan-123", mock_token)

        assert result["title"] == "修复错误"


class TestBackwardCompatibility:
    """Tests to ensure new functions don't break existing functionality"""

    def test_both_functions_coexist(self, mock_token, mock_task_id, mock_task, mocker):
        """Test that both get_task_details and resolve_task work"""
        from planner_lib.task_operations import resolve_task

        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.return_value = mock_task

        # Both should work with GUID
        result1 = get_task_details(mock_task_id, mock_token)
        result2 = resolve_task(mock_token, mock_task_id)

        assert result1["id"] == result2["id"]

    def test_find_task_by_title_matches_resolve_task(self, mock_token, mock_tasks, mocker):
        """Test that find_task_by_title produces same result as resolve_task"""
        from planner_lib.task_operations import resolve_task

        mock_list = mocker.patch("planner_lib.task_operations.list_tasks")
        mock_list.return_value = mock_tasks

        result1 = find_task_by_title("Fix Login Bug", "plan-123", mock_token)
        
        # Reset mock for second call
        mock_list.reset_mock()
        mock_list.return_value = mock_tasks
        
        result2 = resolve_task(mock_token, "Fix Login Bug", plan_id="plan-123")

        assert result1["id"] == result2["id"]
        assert result1["title"] == result2["title"]

