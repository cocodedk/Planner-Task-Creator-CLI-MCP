"""
Basic user search functionality tests
"""

from unittest.mock import patch
from planner_lib.resolution_users import search_users_by_name
from .test_user_search_fixtures import (
    mock_user_search_response,
    get_single_user,
    get_multiple_users
)


class TestSearchUsersByName:
    """Test user search functionality"""

    @patch('planner_lib.resolution_users.search.get_json')
    def test_search_single_result(self, mock_get_json):
        """Test search with single matching user"""
        mock_get_json.return_value = mock_user_search_response([get_single_user()])

        results = search_users_by_name("fake-token", "Iman")

        assert len(results) == 1
        assert results[0]["displayName"] == "Iman Karimi"
        assert results[0]["id"] == "user-id-1"

    @patch('planner_lib.resolution_users.search.get_json')
    def test_search_multiple_results(self, mock_get_json):
        """Test search with multiple matching users"""
        mock_get_json.return_value = mock_user_search_response(get_multiple_users())

        results = search_users_by_name("fake-token", "John")

        assert len(results) == 2
        assert results[0]["displayName"] == "John Smith"
        assert results[1]["displayName"] == "John Doe"

    @patch('planner_lib.resolution_users.search.get_json')
    def test_search_no_results(self, mock_get_json):
        """Test search with no matching users"""
        mock_get_json.return_value = {"value": []}

        results = search_users_by_name("fake-token", "NonExistentUser")

        assert len(results) == 0

    @patch('planner_lib.resolution_users.search.get_json')
    def test_search_api_error(self, mock_get_json):
        """Test search handles API errors gracefully"""
        mock_get_json.side_effect = Exception("API Error")

        results = search_users_by_name("fake-token", "Test")

        # Should return empty list on error
        assert len(results) == 0


