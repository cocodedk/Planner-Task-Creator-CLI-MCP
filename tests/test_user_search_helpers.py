"""
Helper functions for user search tests
"""

import json


def assert_user_not_found_error(error, identifier):
    """Assert that error is a UserNotFound error"""
    assert error["code"] == "UserNotFound"
    assert identifier in error["message"]


def assert_ambiguous_user_error(error, identifier, expected_count):
    """Assert that error is an AmbiguousUser error"""
    assert error["code"] == "AmbiguousUser"
    assert identifier in error["message"]
    assert "suggestions" in error
    assert len(error["suggestions"]) == expected_count


def assert_batch_error(error, expected_not_found=0, expected_ambiguous=0, expected_resolved=0):
    """Assert that error is a BatchUserResolutionError with expected counts"""
    assert error["code"] == "BatchUserResolutionError"
    
    if expected_not_found > 0:
        assert error["notFoundCount"] == expected_not_found
        assert len(error["notFound"]) == expected_not_found
    
    if expected_ambiguous > 0:
        assert error["ambiguousCount"] == expected_ambiguous
        assert len(error["ambiguous"]) == expected_ambiguous
    
    if expected_resolved > 0:
        assert error["resolvedCount"] == expected_resolved
        assert len(error["resolved"]) == expected_resolved
    
    assert "hint" in error


def parse_error(exc_info):
    """Parse ValueError to JSON error object"""
    return json.loads(str(exc_info.value))


