"""
Tests for label parsing functionality
"""

from planner_lib.task_creation import parse_labels


def test_parse_labels_empty():
    """Test parsing empty labels"""
    assert parse_labels(None) == {}
    assert parse_labels("") == {}
    assert parse_labels("   ") == {}


def test_parse_labels_single():
    """Test parsing single label"""
    result = parse_labels("Label1")
    assert result == {"category1": True}


def test_parse_labels_multiple():
    """Test parsing multiple labels"""
    result = parse_labels("Label1,Label3,Label5")
    assert result == {"category1": True, "category3": True, "category5": True}


def test_parse_labels_case_insensitive():
    """Test case-insensitive label parsing"""
    result = parse_labels("label2,LABEL4")
    assert result == {"category2": True, "category4": True}


def test_parse_labels_with_spaces():
    """Test parsing labels with spaces"""
    result = parse_labels("Label1, Label2 , Label3")
    assert result == {"category1": True, "category2": True, "category3": True}


def test_parse_labels_invalid():
    """Test parsing invalid labels (should be filtered out)"""
    result = parse_labels("Label1,NotALabel,Label2")
    assert result == {"category1": True, "category2": True}


