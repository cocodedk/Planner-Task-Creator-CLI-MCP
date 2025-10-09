"""
Utility functions for user resolution
"""

import json
from typing import List, Dict, Any


def format_user_suggestion(user: Dict[str, Any]) -> str:
    """
    Format a user object into a suggestion string.

    Args:
        user: User object from Graph API

    Returns:
        Formatted string like "Display Name (email@example.com)"
    """
    display_name = user.get("displayName", "Unknown")
    email = user.get("mail") or user.get("userPrincipalName", "")
    return f"{display_name} ({email})"


def create_ambiguous_user_error(
    user_identifier: str,
    suggestions: List[str]
) -> ValueError:
    """
    Create an AmbiguousUser error with suggestions.

    Args:
        user_identifier: The ambiguous user identifier
        suggestions: List of suggestion strings

    Returns:
        ValueError with JSON error payload
    """
    error = {
        "code": "AmbiguousUser",
        "message": f"Multiple users found matching '{user_identifier}'. Please be more specific.",
        "suggestions": suggestions,
        "hint": "Use full email address or User ID for exact match"
    }
    return ValueError(json.dumps(error))


def create_user_not_found_error(user_identifier: str) -> ValueError:
    """
    Create a UserNotFound error.

    Args:
        user_identifier: The user identifier that wasn't found

    Returns:
        ValueError with JSON error payload
    """
    error = {
        "code": "UserNotFound",
        "message": f"No users found matching '{user_identifier}'"
    }
    return ValueError(json.dumps(error))


def create_batch_error(
    resolved_info: List[Dict[str, str]],
    not_found: List[str],
    ambiguous: Dict[str, List[str]]
) -> ValueError:
    """
    Create a BatchUserResolutionError with detailed information.

    Args:
        resolved_info: List of successfully resolved users
        not_found: List of user identifiers not found
        ambiguous: Dict mapping ambiguous identifiers to suggestions

    Returns:
        ValueError with JSON error payload
    """
    error = {
        "code": "BatchUserResolutionError",
        "message": f"Failed to resolve {len(not_found) + len(ambiguous)} user identifier(s)"
    }

    if resolved_info:
        error["resolved"] = resolved_info
        error["resolvedCount"] = len(resolved_info)

    if not_found:
        error["notFound"] = not_found
        error["notFoundCount"] = len(not_found)

    if ambiguous:
        error["ambiguous"] = ambiguous
        error["ambiguousCount"] = len(ambiguous)

    error["hint"] = "Please use full email addresses or User IDs for ambiguous/not-found identifiers"

    return ValueError(json.dumps(error))

