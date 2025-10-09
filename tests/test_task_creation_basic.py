"""
Tests for basic task creation functionality
"""

from planner_lib.task_creation import create_task
from .test_task_creation_fixtures import get_mock_task_response


def test_create_task_minimal(mocker, mock_token, mock_requests):
    """Test creating task with minimal fields"""
    mock_requests["response"].json.return_value = get_mock_task_response()

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task"
    )

    assert result["taskId"] == "task-id-123"
    assert result["bucketId"] == "bucket-id-1"

    # Verify POST was called
    mock_requests["post"].assert_called_once()
    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert payload["title"] == "Test Task"
    assert payload["planId"] == "plan-id-1"
    assert payload["bucketId"] == "bucket-id-1"


def test_create_task_with_due_date(mocker, mock_token, mock_requests):
    """Test creating task with due date"""
    mock_requests["response"].json.return_value = get_mock_task_response()

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        due_date="2024-12-31"
    )

    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert payload["dueDateTime"] == "2024-12-31T17:00:00Z"


def test_create_task_with_labels(mocker, mock_token, mock_requests):
    """Test creating task with labels"""
    mock_requests["response"].json.return_value = get_mock_task_response()

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        labels="Label1,Label3"
    )

    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert payload["appliedCategories"] == {"category1": True, "category3": True}


def test_create_task_without_assignee(mocker, mock_token, mock_requests):
    """Test creating task without assignee (backward compatibility)"""
    mock_requests["response"].json.return_value = get_mock_task_response()

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task"
    )

    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert "assignments" not in payload


