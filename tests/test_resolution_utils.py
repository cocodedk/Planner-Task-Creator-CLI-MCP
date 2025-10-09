"""
Tests for resolution utility functions
"""

from planner_lib.resolution import case_insensitive_match


def test_case_insensitive_match():
    """Test case-insensitive matching"""
    items = [
        {"name": "Test Item", "id": "1"},
        {"name": "Another Item", "id": "2"},
        {"name": "TEST ITEM", "id": "3"}
    ]

    matches = case_insensitive_match(items, "name", "test item")
    assert len(matches) == 2
    assert matches[0]["id"] == "1"
    assert matches[1]["id"] == "3"


