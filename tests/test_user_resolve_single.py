"""
Single user resolution tests
"""

import pytest
from unittest.mock import patch
from planner_lib.resolution_users import resolve_user
from .test_user_search_fixtures import get_single_user, get_multiple_users
from .test_user_search_helpers import parse_error, assert_ambiguous_user_error


class TestResolveUser:
    """Test user resolution with search fallback"""

    def test_resolve_guid_directly(self):
        """Test that GUIDs are returned without API calls"""
        guid = "12345678-1234-1234-1234-123456789012"

        result = resolve_user("fake-token", guid)

        assert result == guid

    @patch('planner_lib.resolution_users.resolver.get_json')
    def test_resolve_exact_email_match(self, mock_get_json):
        """Test exact email match resolution"""
        user = get_single_user()
        mock_get_json.return_value = user

        result = resolve_user("fake-token", "test@company.com")

        assert result == "user-id-1"
        # Verify exact match URL was called
        mock_get_json.assert_called_once()
        call_args = mock_get_json.call_args[0]
        assert "users/test@company.com" in call_args[0]

    @patch('planner_lib.resolution_users.resolver.search_users_by_name')
    @patch('planner_lib.resolution_users.resolver.get_json')
    def test_resolve_single_search_match(self, mock_get_json, mock_search):
        """Test resolution falls back to search with single match"""
        # Exact match fails
        mock_get_json.side_effect = Exception("Not found")

        # Search returns single match
        mock_search.return_value = [get_single_user()]

        result = resolve_user("fake-token", "Iman", enable_search=True)

        assert result == "user-id-1"
        mock_search.assert_called_once_with("fake-token", "Iman")

    @patch('planner_lib.resolution_users.resolver.search_users_by_name')
    @patch('planner_lib.resolution_users.resolver.get_json')
    def test_resolve_ambiguous_search(self, mock_get_json, mock_search):
        """Test resolution raises error on multiple search matches"""
        # Exact match fails
        mock_get_json.side_effect = Exception("Not found")

        # Search returns multiple matches
        mock_search.return_value = get_multiple_users()

        with pytest.raises(ValueError) as exc_info:
            resolve_user("fake-token", "John", enable_search=True)

        error = parse_error(exc_info)
        assert_ambiguous_user_error(error, "John", 2)

    @patch('planner_lib.resolution_users.resolver.search_users_by_name')
    @patch('planner_lib.resolution_users.resolver.get_json')
    def test_resolve_not_found_no_search(self, mock_get_json, mock_search):
        """Test user not found when search is disabled"""
        # Exact match fails
        mock_get_json.side_effect = Exception("Not found")

        with pytest.raises(ValueError) as exc_info:
            resolve_user("fake-token", "NonExistent", enable_search=False)

        error = parse_error(exc_info)
        assert error["code"] == "UserNotFound"
        assert "not found or not accessible" in error["message"]

        # Search should not have been called
        mock_search.assert_not_called()

    @patch('planner_lib.resolution_users.resolver.search_users_by_name')
    @patch('planner_lib.resolution_users.resolver.get_json')
    def test_resolve_not_found_with_search(self, mock_get_json, mock_search):
        """Test user not found even with search enabled"""
        # Exact match fails
        mock_get_json.side_effect = Exception("Not found")

        # Search returns no results
        mock_search.return_value = []

        with pytest.raises(ValueError) as exc_info:
            resolve_user("fake-token", "NonExistent", enable_search=True)

        error = parse_error(exc_info)
        assert error["code"] == "UserNotFound"
        assert "No users found matching" in error["message"]
