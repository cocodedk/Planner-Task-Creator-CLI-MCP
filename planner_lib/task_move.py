"""
Task Move Module
Move tasks between buckets.
"""

import requests

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, patch_json


def move_task_op(task_id: str, bucket_id: str, token: str) -> dict:
    """
    Move a task to a different bucket.

    Args:
        task_id: Task ID
        bucket_id: Target bucket ID
        token: Access token

    Returns:
        Updated task object or success dict

    Raises:
        requests.RequestException: On API errors
    """
    # Fetch current task for ETag
    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    task = get_json(url, token)
    etag = task["@odata.etag"]

    # Update with retry on ETag conflict
    try:
        result = patch_json(url, token, {"bucketId": bucket_id}, etag)
        return result if result else {"ok": True, "taskId": task_id}
    except requests.HTTPError as e:
        if e.response.status_code == 412:
            # Retry once
            task = get_json(url, token)
            etag = task["@odata.etag"]
            result = patch_json(url, token, {"bucketId": bucket_id}, etag)
            return result if result else {"ok": True, "taskId": task_id}
        raise
