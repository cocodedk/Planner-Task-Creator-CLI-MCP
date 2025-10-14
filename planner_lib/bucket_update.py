"""
Bucket Update Module
Update bucket properties in Microsoft Planner.
"""

import requests

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, patch_json


def update_bucket_op(bucket_id: str, new_name: str, token: str) -> dict:
    """
    Update a bucket's name.

    Args:
        bucket_id: Bucket ID
        new_name: New bucket name
        token: Access token

    Returns:
        Dictionary with ok, bucketId, oldName, newName

    Raises:
        requests.RequestException: On API errors
    """
    # Fetch current bucket for ETag and old name
    url = f"{BASE_GRAPH_URL}/planner/buckets/{bucket_id}"
    bucket = get_json(url, token)
    etag = bucket["@odata.etag"]
    old_name = bucket["name"]

    # Update with retry on ETag conflict
    try:
        patch_json(url, token, {"name": new_name}, etag)
    except requests.HTTPError as e:
        if e.response.status_code == 412:
            # Retry once on ETag conflict
            bucket = get_json(url, token)
            etag = bucket["@odata.etag"]
            patch_json(url, token, {"name": new_name}, etag)
        else:
            raise

    return {
        "ok": True,
        "bucketId": bucket_id,
        "oldName": old_name,
        "newName": new_name
    }
