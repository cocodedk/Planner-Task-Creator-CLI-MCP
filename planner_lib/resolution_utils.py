"""
Resolution Utilities Module
Common utility functions for resolution operations.
"""

from typing import List


def case_insensitive_match(items: List[dict], key: str, value: str) -> List[dict]:
    """Filter list of dictionaries by case-insensitive key value match."""
    value_lower = value.lower()
    return [item for item in items if item.get(key, "").lower() == value_lower]
