"""
Tests for task creation with descriptions
"""

from planner_lib.task_creation import create_task
from .test_task_creation_fixtures import (
    get_mock_task_response,
    get_mock_task_details_response
)


def test_create_task_with_description(mocker, mock_token, mock_requests):
    """Test creating task with description"""
    # First call returns task, second returns details with etag
    mock_requests["response"].json.side_effect = [
        get_mock_task_response(),
        get_mock_task_details_response(),
        {}
    ]

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        description="This is a test description"
    )

    # Verify POST and PATCH were called
    assert mock_requests["post"].call_count == 1
    assert mock_requests["get"].call_count == 1
    assert mock_requests["patch"].call_count == 1

    # Verify PATCH payload
    patch_call = mock_requests["patch"].call_args
    assert patch_call[1]["json"]["description"] == "This is a test description"


def test_create_task_all_fields(mocker, mock_token, mock_requests):
    """Test creating task with all optional fields"""
    mock_requests["response"].json.side_effect = [
        get_mock_task_response(),
        get_mock_task_details_response(),
        {}
    ]

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Complete Task",
        description="Full description",
        due_date="2024-12-31",
        labels="Label1,Label2"
    )

    # Verify task was created with all fields
    post_call = mock_requests["post"].call_args
    payload = post_call[1]["json"]

    assert payload["title"] == "Complete Task"
    assert payload["dueDateTime"] == "2024-12-31T17:00:00Z"
    assert payload["appliedCategories"] == {"category1": True, "category2": True}


