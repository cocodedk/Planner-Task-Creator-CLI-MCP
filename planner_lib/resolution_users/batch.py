"""
Batch user resolution with comprehensive error reporting
"""

import json
from typing import List

from .resolver import resolve_user
from .utils import create_batch_error


def resolve_users(token: str, assignee_csv: str) -> List[str]:
    """
    Parse comma-separated user identifiers and resolve all to User IDs.

    Uses batch validation: attempts to resolve all identifiers first,
    then reports all errors together instead of failing on first error.

    Args:
        token: OAuth access token
        assignee_csv: Comma-separated emails/UPNs/User IDs/partial names

    Returns:
        List of User IDs (GUIDs)

    Raises:
        ValueError: If any user resolution fails, with detailed batch error report
    """
    if not assignee_csv:
        return []

    # Split and clean
    identifiers = [user.strip() for user in assignee_csv.split(",") if user.strip()]

    # Batch validation: try to resolve all users and collect results/errors
    user_ids = []
    resolved_info = []  # Successfully resolved users
    not_found = []      # Users not found
    ambiguous = {}      # Users with multiple matches

    for identifier in identifiers:
        try:
            user_id = resolve_user(token, identifier)
            user_ids.append(user_id)
            resolved_info.append({
                "input": identifier,
                "userId": user_id
            })
        except ValueError as e:
            try:
                error_data = json.loads(str(e))

                if error_data.get("code") == "AmbiguousUser":
                    # Collect ambiguous user with suggestions
                    ambiguous[identifier] = error_data.get("suggestions", [])
                elif error_data.get("code") == "UserNotFound":
                    # Collect not found user
                    not_found.append(identifier)
                else:
                    # Unknown error, re-raise
                    raise
            except (json.JSONDecodeError, KeyError):
                # Not a JSON error, re-raise
                raise

    # If there are any errors, report all of them together
    if not_found or ambiguous:
        raise create_batch_error(resolved_info, not_found, ambiguous)

    return user_ids

