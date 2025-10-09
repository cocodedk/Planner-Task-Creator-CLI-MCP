"""
Tests for list_tasks function
"""

import pytest
from planner_lib.task_operations import list_tasks


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
        },
        {
            "id": "task-id-3",
            "title": "Task Three",
            "bucketId": "bucket-id-2",
            "planId": "plan-id-1",
            "percentComplete": 100
        }
    ]


class TestListTasks:
    """Tests for list_tasks function"""

    def test_list_tasks_by_plan(self, mock_token, mock_tasks, mocker):
        """Test listing tasks by plan ID"""
        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.return_value = {"value": mock_tasks}

        result = list_tasks(mock_token, plan_id="plan-id-1")

        assert len(result) == 3
        assert result[0]["title"] == "Task One"
        mock_get.assert_called_once()

    def test_list_tasks_by_bucket(self, mock_token, mock_tasks, mocker):
        """Test listing tasks by bucket ID"""
        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.return_value = {"value": mock_tasks}

        result = list_tasks(mock_token, bucket_id="bucket-id-1")

        assert len(result) == 3
        mock_get.assert_called_once()

    def test_list_tasks_incomplete_only(self, mock_token, mock_tasks, mocker):
        """Test filtering incomplete tasks"""
        mock_get = mocker.patch("planner_lib.task_operations.get_json")
        mock_get.return_value = {"value": mock_tasks}

        result = list_tasks(mock_token, plan_id="plan-id-1", incomplete_only=True)

        assert len(result) == 2
        assert all(t["percentComplete"] < 100 for t in result)

    def test_list_tasks_no_params_raises_error(self, mock_token):
        """Test that missing plan_id and bucket_id raises error"""
        with pytest.raises(ValueError, match="plan_id or bucket_id required"):
            list_tasks(mock_token)
