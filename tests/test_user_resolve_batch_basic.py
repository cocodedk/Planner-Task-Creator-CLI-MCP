"""
Basic batch user resolution tests
"""

import pytest
import json
from unittest.mock import patch
from planner_lib.resolution_users import resolve_users
from .test_user_search_helpers import parse_error, assert_batch_error


class TestResolveUsers:
    """Test batch user resolution"""

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_resolve_multiple_users(self, mock_resolve):
        """Test resolving comma-separated users"""
        mock_resolve.side_effect = ["user-id-1", "user-id-2", "user-id-3"]

        result = resolve_users("fake-token", "user1@company.com,user2@company.com,user3@company.com")

        assert len(result) == 3
        assert result == ["user-id-1", "user-id-2", "user-id-3"]
        assert mock_resolve.call_count == 3

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_resolve_mixed_identifiers(self, mock_resolve):
        """Test resolving mix of emails and names"""
        mock_resolve.side_effect = ["user-id-1", "user-id-2"]

        result = resolve_users("fake-token", "user1@company.com,Iman")

        assert len(result) == 2
        assert mock_resolve.call_count == 2

        # Check that both identifiers were passed
        calls = mock_resolve.call_args_list
        assert calls[0][0][1] == "user1@company.com"
        assert calls[1][0][1] == "Iman"

    def test_resolve_empty_string(self):
        """Test empty string returns empty list"""
        result = resolve_users("fake-token", "")

        assert result == []

    def test_resolve_whitespace_only(self):
        """Test whitespace-only string returns empty list"""
        result = resolve_users("fake-token", "   ,  , ")

        assert result == []

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_resolve_strips_whitespace(self, mock_resolve):
        """Test that whitespace is properly stripped"""
        mock_resolve.side_effect = ["user-id-1", "user-id-2"]

        result = resolve_users("fake-token", " user1@company.com , user2@company.com ")

        assert len(result) == 2

        # Verify identifiers were stripped
        calls = mock_resolve.call_args_list
        assert calls[0][0][1] == "user1@company.com"
        assert calls[1][0][1] == "user2@company.com"

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_resolve_single_error_reported(self, mock_resolve):
        """Test that single resolution error is reported in batch format"""
        mock_resolve.side_effect = ValueError(json.dumps({
            "code": "UserNotFound",
            "message": "User not found"
        }))

        with pytest.raises(ValueError) as exc_info:
            resolve_users("fake-token", "nonexistent@company.com")

        error = parse_error(exc_info)
        assert_batch_error(error, expected_not_found=1)
        assert "nonexistent@company.com" in error["notFound"]


