"""
Tests for task creation with assignments
"""

from planner_lib.task_creation import create_task
from .test_helpers import get_test_user_id_1, get_test_user_id_2
from .test_task_creation_fixtures import get_mock_task_response


def test_create_task_with_assignee(mocker, mock_token, mock_requests):
    """Test creating task with assignee"""
    user_id = get_test_user_id_1()

    # Mock resolve_users
    mocker.patch('planner_lib.task_creation.resolve_users', return_value=[user_id])
    mock_requests["response"].json.return_value = get_mock_task_response()

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        assignee="user@example.com"
    )

    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert "assignments" in payload
    assert user_id in payload["assignments"]
    assert payload["assignments"][user_id]["@odata.type"] == "#microsoft.graph.plannerAssignment"


def test_create_task_with_multiple_assignees(mocker, mock_token, mock_requests):
    """Test creating task with multiple assignees"""
    user_id1 = get_test_user_id_1()
    user_id2 = get_test_user_id_2()

    # Mock resolve_users
    mocker.patch('planner_lib.task_creation.resolve_users', return_value=[user_id1, user_id2])
    mock_requests["response"].json.return_value = get_mock_task_response()

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        assignee="user1@example.com,user2@example.com"
    )

    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert "assignments" in payload
    assert len(payload["assignments"]) == 2
    assert user_id1 in payload["assignments"]
    assert user_id2 in payload["assignments"]


