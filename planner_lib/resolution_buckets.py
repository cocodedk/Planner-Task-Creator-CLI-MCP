"""
Bucket Resolution Module
Handles listing and resolving bucket names to IDs.
"""

import json
from typing import List

from .constants import BASE_GRAPH_URL, GUID_PATTERN
from .graph_client import get_json
from .resolution_utils import case_insensitive_match


def list_plan_buckets(plan_id: str, token: str) -> List[dict]:
    """
    List all buckets in a specific plan.

    Args:
        plan_id: Plan ID
        token: Access token

    Returns:
        List of bucket objects
    """
    url = f"{BASE_GRAPH_URL}/planner/plans/{plan_id}/buckets"
    data = get_json(url, token)
    return data.get("value", [])


def resolve_bucket(token: str, plan_id: str, bucket: str) -> dict:
    """
    Resolve bucket name or ID to bucket object.

    Args:
        token: Access token
        plan_id: Plan ID
        bucket: Bucket name or ID

    Returns:
        Bucket object with 'id' field

    Raises:
        ValueError: With JSON error object if not found or ambiguous
    """
    # Check if input is a GUID
    if GUID_PATTERN.match(bucket):
        return {"id": bucket}

    # Fetch all buckets
    buckets = list_plan_buckets(plan_id, token)

    # Find case-insensitive matches
    matches = case_insensitive_match(buckets, "name", bucket)

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        candidates = [{"id": b["id"], "name": b["name"]} for b in matches]
        error = {
            "code": "Ambiguous",
            "message": f"Multiple buckets match '{bucket}'",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))
    else:
        candidates = [{"id": b["id"], "name": b["name"]} for b in buckets]
        error = {
            "code": "NotFound",
            "message": f"Bucket '{bucket}' not found",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))
