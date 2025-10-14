"""
Bucket Create Module
Create new buckets in Microsoft Planner.
"""

from .constants import BASE_GRAPH_URL
from .graph_client import post_json


def create_bucket_op(plan_id: str, name: str, token: str) -> dict:
    """
    Create a new bucket in a plan.

    Args:
        plan_id: Plan ID
        name: Bucket name
        token: Access token

    Returns:
        Dictionary with ok, bucketId, name, planId

    Raises:
        requests.RequestException: On API errors
    """
    # Build payload
    payload = {
        "name": name,
        "planId": plan_id,
        "orderHint": " !"  # Default order hint (at the end)
    }

    # Create bucket
    url = f"{BASE_GRAPH_URL}/planner/buckets"
    bucket = post_json(url, token, payload)

    return {
        "ok": True,
        "bucketId": bucket["id"],
        "name": bucket["name"],
        "planId": bucket["planId"]
    }
