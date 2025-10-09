"""
Batch user resolution error handling tests
"""

import pytest
import json
from unittest.mock import patch
from planner_lib.resolution_users import resolve_users
from .test_user_search_helpers import parse_error, assert_batch_error


class TestBatchUserResolution:
    """Test batch validation for multiple users"""

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_batch_all_ambiguous(self, mock_resolve):
        """Test batch error when all users are ambiguous"""
        def side_effect(token, identifier):
            raise ValueError(json.dumps({
                "code": "AmbiguousUser",
                "message": f"Multiple users found matching '{identifier}'",
                "suggestions": [f"{identifier} User 1", f"{identifier} User 2"]
            }))

        mock_resolve.side_effect = side_effect

        with pytest.raises(ValueError) as exc_info:
            resolve_users("fake-token", "John,Chris,Alex")

        error = parse_error(exc_info)
        assert_batch_error(error, expected_ambiguous=3)
        assert "John" in error["ambiguous"]
        assert "Chris" in error["ambiguous"]
        assert "Alex" in error["ambiguous"]
        assert len(error["ambiguous"]["John"]) == 2

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_batch_all_not_found(self, mock_resolve):
        """Test batch error when all users are not found"""
        mock_resolve.side_effect = ValueError(json.dumps({
            "code": "UserNotFound",
            "message": "User not found"
        }))

        with pytest.raises(ValueError) as exc_info:
            resolve_users("fake-token", "invalid1@test.com,invalid2@test.com,invalid3@test.com")

        error = parse_error(exc_info)
        assert_batch_error(error, expected_not_found=3)
        assert "invalid1@test.com" in error["notFound"]
        assert "invalid2@test.com" in error["notFound"]
        assert "invalid3@test.com" in error["notFound"]

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_batch_partial_success_still_fails(self, mock_resolve):
        """Test that even with some successes, any error fails the batch"""
        mock_resolve.side_effect = [
            "user-id-1",  # Success
            "user-id-2",  # Success
            ValueError(json.dumps({"code": "UserNotFound", "message": "Not found"})),  # Fail
        ]

        with pytest.raises(ValueError) as exc_info:
            resolve_users("fake-token", "user1@test.com,user2@test.com,invalid@test.com")

        error = parse_error(exc_info)
        assert_batch_error(error, expected_resolved=2, expected_not_found=1)


