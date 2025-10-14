"""
Bucket Delete Module
Delete buckets from Microsoft Planner.
"""

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, delete_json


def delete_bucket_op(bucket_id: str, token: str) -> dict:
    """
    Delete a bucket.

    Args:
        bucket_id: Bucket ID
        token: Access token

    Returns:
        Success dict with ok and bucketId

    Raises:
        requests.RequestException: On API errors
    """
    # Fetch current bucket for ETag
    url = f"{BASE_GRAPH_URL}/planner/buckets/{bucket_id}"
    bucket = get_json(url, token)
    etag = bucket["@odata.etag"]

    # Delete with ETag
    delete_json(url, token, etag)

    return {
        "ok": True,
        "bucketId": bucket_id
    }
