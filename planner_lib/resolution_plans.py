"""
Plan Resolution Module
Handles listing and resolving plan names to IDs.
"""

import json
from typing import List

from .constants import BASE_GRAPH_URL, GUID_PATTERN
from .graph_client import get_json
from .resolution_utils import case_insensitive_match


def list_user_plans(token: str) -> List[dict]:
    """
    List all plans accessible to the user with group names.

    Args:
        token: Access token

    Returns:
        List of plan objects with optional groupName field
    """
    url = f"{BASE_GRAPH_URL}/me/planner/plans"
    data = get_json(url, token)
    plans = data.get("value", [])

    # Augment with group names
    for plan in plans:
        owner_id = plan.get("owner")
        if owner_id:
            try:
                group_url = f"{BASE_GRAPH_URL}/groups/{owner_id}"
                group_data = get_json(group_url, token)
                plan["groupName"] = group_data.get("displayName", "")
            except Exception:
                pass

    return plans


def resolve_plan(token: str, plan: str) -> dict:
    """
    Resolve plan name or ID to plan object.

    Args:
        token: Access token
        plan: Plan name or ID

    Returns:
        Plan object with 'id' field

    Raises:
        ValueError: With JSON error object if not found or ambiguous
    """
    # Check if input is a GUID
    if GUID_PATTERN.match(plan):
        return {"id": plan}

    # Fetch all plans
    plans = list_user_plans(token)

    # Find case-insensitive matches
    matches = case_insensitive_match(plans, "title", plan)

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        candidates = [{"id": p["id"], "title": p["title"], "groupName": p.get("groupName", "")}
                     for p in matches]
        error = {
            "code": "Ambiguous",
            "message": f"Multiple plans match '{plan}'",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))
    else:
        candidates = [{"id": p["id"], "title": p["title"], "groupName": p.get("groupName", "")}
                     for p in plans]
        error = {
            "code": "NotFound",
            "message": f"Plan '{plan}' not found",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))
