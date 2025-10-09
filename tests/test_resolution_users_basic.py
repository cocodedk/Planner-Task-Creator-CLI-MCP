"""
Basic user resolution tests
"""

import pytest
from unittest.mock import patch
import json

from planner_lib.resolution_users import resolve_user, resolve_users
from .test_helpers import get_test_user_id_1, get_test_user_id_2


def test_resolve_user_with_guid():
    """Test that GUID passes through without API call"""
    token = "test_token"
    user_id = get_test_user_id_1()

    result = resolve_user(token, user_id)

    assert result == user_id


@patch('planner_lib.resolution_users.resolver.get_json')
def test_resolve_user_with_email(mock_get_json):
    """Test resolving user by email"""
    token = "test_token"
    email = "user@example.com"
    user_id = get_test_user_id_1()

    mock_get_json.return_value = {"id": user_id, "userPrincipalName": email}

    result = resolve_user(token, email)

    assert result == user_id
    mock_get_json.assert_called_once_with(
        f"https://graph.microsoft.com/v1.0/users/{email}",
        token
    )


@patch('planner_lib.resolution_users.search.search_users_by_name')
@patch('planner_lib.resolution_users.resolver.get_json')
def test_resolve_user_not_found(mock_get_json, mock_search):
    """Test error handling when user not found"""
    token = "test_token"
    email = "nonexistent@example.com"

    mock_get_json.side_effect = Exception("404 Not Found")
    mock_search.return_value = []

    with pytest.raises(ValueError) as exc_info:
        resolve_user(token, email)

    error = json.loads(str(exc_info.value))
    assert error["code"] == "UserNotFound"
    assert email in error["message"]


def test_resolve_users_empty_string():
    """Test resolving empty string returns empty list"""
    token = "test_token"

    result = resolve_users(token, "")

    assert result == []


def test_resolve_users_single_guid():
    """Test resolving single GUID"""
    token = "test_token"
    user_id = get_test_user_id_1()

    result = resolve_users(token, user_id)

    assert result == [user_id]


def test_resolve_users_whitespace_handling():
    """Test that whitespace is properly handled"""
    token = "test_token"
    user_id1 = get_test_user_id_1()
    user_id2 = get_test_user_id_2()

    result = resolve_users(token, f"  {user_id1}  ,  {user_id2}  ")

    assert result == [user_id1, user_id2]


