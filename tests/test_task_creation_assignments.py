"""
Tests for task assignment functionality
"""

from planner_lib.task_creation import build_assignments
from .test_helpers import get_test_user_id_1, get_test_user_id_2


def test_build_assignments_empty():
    """Test building assignments with empty list"""
    result = build_assignments([])
    assert result == {}


def test_build_assignments_single_user():
    """Test building assignments with single user"""
    user_id = get_test_user_id_1()
    result = build_assignments([user_id])

    assert user_id in result
    assert result[user_id]["@odata.type"] == "#microsoft.graph.plannerAssignment"
    assert result[user_id]["orderHint"] == " !"


def test_build_assignments_multiple_users():
    """Test building assignments with multiple users"""
    user_id1 = get_test_user_id_1()
    user_id2 = get_test_user_id_2()
    result = build_assignments([user_id1, user_id2])

    assert len(result) == 2
    assert user_id1 in result
    assert user_id2 in result
    assert result[user_id1]["orderHint"] == " !"
    assert result[user_id2]["orderHint"] == " !"


