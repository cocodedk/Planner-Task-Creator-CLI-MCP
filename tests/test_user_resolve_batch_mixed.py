"""
Batch user resolution tests with mixed success/error scenarios
"""

import pytest
import json
from unittest.mock import patch
from planner_lib.resolution_users import resolve_users
from .test_user_search_helpers import parse_error, assert_batch_error


class TestBatchMixedScenarios:
    """Test batch error with mix of successful, ambiguous, and not found"""

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_batch_mixed_errors(self, mock_resolve):
        """Test batch error with mix of successful, ambiguous, and not found"""
        def side_effect(token, identifier):
            if identifier == "Iman":
                return "user-id-1"  # Success
            elif identifier == "John":
                raise ValueError(json.dumps({
                    "code": "AmbiguousUser",
                    "message": "Multiple users found",
                    "suggestions": ["John Smith", "John Doe"]
                }))
            elif identifier == "invalid@test.com":
                return "user-id-2"  # Success
            else:  # "nonexistent"
                raise ValueError(json.dumps({
                    "code": "UserNotFound",
                    "message": "User not found"
                }))

        mock_resolve.side_effect = side_effect

        with pytest.raises(ValueError) as exc_info:
            resolve_users("fake-token", "Iman,John,invalid@test.com,nonexistent")

        error = parse_error(exc_info)
        assert error["message"] == "Failed to resolve 2 user identifier(s)"

        # Check resolved users
        assert_batch_error(error, expected_resolved=2, expected_ambiguous=1, expected_not_found=1)
        assert error["resolved"][0]["input"] == "Iman"
        assert error["resolved"][0]["userId"] == "user-id-1"

        # Check ambiguous users
        assert "John" in error["ambiguous"]
        assert len(error["ambiguous"]["John"]) == 2

        # Check not found users
        assert "nonexistent" in error["notFound"]

    @patch('planner_lib.resolution_users.batch.resolve_user')
    def test_batch_multiple_ambiguous_different_suggestions(self, mock_resolve):
        """Test batch with multiple ambiguous users having different suggestions"""
        def side_effect(token, identifier):
            if identifier == "John":
                raise ValueError(json.dumps({
                    "code": "AmbiguousUser",
                    "suggestions": ["John Smith (john.s@test.com)", "John Doe (john.d@test.com)"]
                }))
            elif identifier == "Sarah":
                raise ValueError(json.dumps({
                    "code": "AmbiguousUser",
                    "suggestions": [
                        "Sarah Connor (sarah.c@test.com)",
                        "Sarah Parker (sarah.p@test.com)",
                        "Sarah Lee (sarah.l@test.com)"
                    ]
                }))
            else:
                return "user-id-1"

        mock_resolve.side_effect = side_effect

        with pytest.raises(ValueError) as exc_info:
            resolve_users("fake-token", "John,Iman,Sarah")

        error = parse_error(exc_info)
        assert_batch_error(error, expected_ambiguous=2, expected_resolved=1)
        assert len(error["ambiguous"]["John"]) == 2
        assert len(error["ambiguous"]["Sarah"]) == 3


