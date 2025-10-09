"""
Tests for User Resolution Module
"""

import pytest
from unittest.mock import patch, MagicMock
import json

from planner_lib.resolution_users import resolve_user, resolve_users
from .test_helpers import get_test_user_id_1, get_test_user_id_2


def test_resolve_user_with_guid():
    """Test that GUID passes through without API call"""
    token = "test_token"
    user_id = get_test_user_id_1()
    
    result = resolve_user(token, user_id)
    
    assert result == user_id


@patch('planner_lib.resolution_users.get_json')
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


@patch('planner_lib.resolution_users.get_json')
def test_resolve_user_not_found(mock_get_json):
    """Test error handling when user not found"""
    token = "test_token"
    email = "nonexistent@example.com"

    mock_get_json.side_effect = Exception("404 Not Found")

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


@patch('planner_lib.resolution_users.get_json')
def test_resolve_users_multiple_emails(mock_get_json):
    """Test resolving multiple emails"""
    token = "test_token"
    email1 = "user1@example.com"
    email2 = "user2@example.com"
    user_id1 = get_test_user_id_1()
    user_id2 = get_test_user_id_2()
    
    def mock_response(url, token):
        if email1 in url:
            return {"id": user_id1}
        elif email2 in url:
            return {"id": user_id2}
    
    mock_get_json.side_effect = mock_response
    
    result = resolve_users(token, f"{email1},{email2}")
    
    assert result == [user_id1, user_id2]
    assert mock_get_json.call_count == 2


@patch('planner_lib.resolution_users.get_json')
def test_resolve_users_mixed_identifiers(mock_get_json):
    """Test resolving mixed emails and GUIDs"""
    token = "test_token"
    email = "user1@example.com"
    user_id_input = get_test_user_id_2()
    user_id_resolved = get_test_user_id_1()
    
    mock_get_json.return_value = {"id": user_id_resolved}
    
    result = resolve_users(token, f"{email}, {user_id_input}")
    
    assert result == [user_id_resolved, user_id_input]
    mock_get_json.assert_called_once()  # Only called for email, not GUID


@patch('planner_lib.resolution_users.get_json')
def test_resolve_users_first_fails(mock_get_json):
    """Test that first resolution error propagates"""
    token = "test_token"
    email1 = "invalid@example.com"
    email2 = "user2@example.com"

    mock_get_json.side_effect = Exception("404 Not Found")

    with pytest.raises(ValueError) as exc_info:
        resolve_users(token, f"{email1},{email2}")

    error = json.loads(str(exc_info.value))
    assert error["code"] == "UserNotFound"
    # Should fail on first user, not reach second
    assert mock_get_json.call_count == 1


def test_resolve_users_whitespace_handling():
    """Test that whitespace is properly handled"""
    token = "test_token"
    user_id1 = get_test_user_id_1()
    user_id2 = get_test_user_id_2()
    
    result = resolve_users(token, f"  {user_id1}  ,  {user_id2}  ")
    
    assert result == [user_id1, user_id2]
