"""
Single user resolution logic
"""

import json
from typing import Optional

from ..constants import BASE_GRAPH_URL, GUID_PATTERN
from ..graph_client import get_json
from .search import search_users_by_name
from .utils import (
    format_user_suggestion,
    create_ambiguous_user_error,
    create_user_not_found_error
)


def resolve_user(token: str, user_identifier: str, enable_search: bool = True) -> str:
    """
    Resolve user email/UPN, User ID, or partial name to Azure AD User ID (GUID).

    Resolution strategy:
    1. If input is a GUID, return it directly
    2. Try exact match (email/UPN lookup)
    3. If enable_search=True and exact match fails, try partial name search
       - If exactly 1 match found, use it
       - If multiple matches found, raise AmbiguousUser error with suggestions

    Args:
        token: OAuth access token
        user_identifier: Email/UPN, User ID (GUID), or partial name
        enable_search: Enable partial name search fallback (default: True)

    Returns:
        User ID (GUID) as string

    Raises:
        ValueError: With JSON error object if user not found or ambiguous
    """
    user_identifier = user_identifier.strip()

    # Step 1: Check if input is already a GUID
    if GUID_PATTERN.match(user_identifier):
        return user_identifier

    # Step 2: Try exact match (email/UPN)
    try:
        url = f"{BASE_GRAPH_URL}/users/{user_identifier}"
        user = get_json(url, token)
        return user["id"]
    except Exception:
        # Exact match failed, try search if enabled
        if not enable_search:
            error = {
                "code": "UserNotFound",
                "message": f"User '{user_identifier}' not found or not accessible"
            }
            raise ValueError(json.dumps(error))

    # Step 3: Try partial name search
    search_results = search_users_by_name(token, user_identifier)

    if len(search_results) == 0:
        raise create_user_not_found_error(user_identifier)

    if len(search_results) == 1:
        # Single match - use it
        return search_results[0]["id"]

    # Multiple matches - raise ambiguous error with suggestions
    suggestions = [
        format_user_suggestion(user)
        for user in search_results[:5]  # Limit to first 5 suggestions
    ]

    raise create_ambiguous_user_error(user_identifier, suggestions)
