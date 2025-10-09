"""
Multiple user resolution tests
"""

import pytest
from unittest.mock import patch
import json

from planner_lib.resolution_users import resolve_users
from .test_helpers import get_test_user_id_1, get_test_user_id_2


@patch('planner_lib.resolution_users.batch.resolve_user')
def test_resolve_users_multiple_emails(mock_resolve_user):
    """Test resolving multiple emails"""
    token = "test_token"
    email1 = "user1@example.com"
    email2 = "user2@example.com"
    user_id1 = get_test_user_id_1()
    user_id2 = get_test_user_id_2()

    mock_resolve_user.side_effect = [user_id1, user_id2]

    result = resolve_users(token, f"{email1},{email2}")

    assert result == [user_id1, user_id2]
    assert mock_resolve_user.call_count == 2


@patch('planner_lib.resolution_users.batch.resolve_user')
def test_resolve_users_mixed_identifiers(mock_resolve_user):
    """Test resolving mixed emails and GUIDs"""
    token = "test_token"
    email = "user1@example.com"
    user_id_input = get_test_user_id_2()
    user_id_resolved = get_test_user_id_1()

    mock_resolve_user.side_effect = [user_id_resolved, user_id_input]

    result = resolve_users(token, f"{email}, {user_id_input}")

    assert result == [user_id_resolved, user_id_input]
    assert mock_resolve_user.call_count == 2


@patch('planner_lib.resolution_users.batch.resolve_user')
def test_resolve_users_first_fails(mock_resolve_user):
    """Test that first resolution error is collected in batch error"""
    token = "test_token"
    email1 = "invalid@example.com"
    email2 = "user2@example.com"

    # First user fails, second would succeed but batch validation collects all errors
    mock_resolve_user.side_effect = [
        ValueError(json.dumps({"code": "UserNotFound", "message": "User not found"})),
        "user-id-2"
    ]

    with pytest.raises(ValueError) as exc_info:
        resolve_users(token, f"{email1},{email2}")

    error = json.loads(str(exc_info.value))
    assert error["code"] == "BatchUserResolutionError"
    assert error["notFoundCount"] == 1
    assert error["resolvedCount"] == 1


