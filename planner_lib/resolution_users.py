"""
User Resolution Module
Handles resolving user emails/UPNs to Azure AD User IDs.
"""

import json
import re
from typing import List

from .constants import BASE_GRAPH_URL, GUID_PATTERN
from .graph_client import get_json


def resolve_user(token: str, user_identifier: str) -> str:
    """
    Resolve user email/UPN or User ID to Azure AD User ID (GUID).

    Args:
        token: OAuth access token
        user_identifier: Email/UPN or User ID (GUID)

    Returns:
        User ID (GUID) as string

    Raises:
        ValueError: With JSON error object if user not found
    """
    # Check if input is already a GUID
    if GUID_PATTERN.match(user_identifier):
        return user_identifier

    # Resolve as email/UPN
    try:
        url = f"{BASE_GRAPH_URL}/users/{user_identifier}"
        user = get_json(url, token)
        return user["id"]
    except Exception as e:
        # User not found or not accessible
        error = {
            "code": "UserNotFound",
            "message": f"User '{user_identifier}' not found or not accessible"
        }
        raise ValueError(json.dumps(error))


def resolve_users(token: str, assignee_csv: str) -> List[str]:
    """
    Parse comma-separated user identifiers and resolve all to User IDs.

    Args:
        token: OAuth access token
        assignee_csv: Comma-separated emails/UPNs/User IDs

    Returns:
        List of User IDs (GUIDs)

    Raises:
        ValueError: If any user resolution fails
    """
    if not assignee_csv:
        return []

    # Split and clean
    identifiers = [user.strip() for user in assignee_csv.split(",") if user.strip()]

    # Resolve each user
    user_ids = []
    for identifier in identifiers:
        user_id = resolve_user(token, identifier)
        user_ids.append(user_id)

    return user_ids
