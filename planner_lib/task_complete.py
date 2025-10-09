"""
Task Complete Module
Mark tasks as complete.
"""

import requests

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, patch_json


def complete_task_op(task_id: str, token: str) -> dict:
    """
    Mark a task as complete.

    Args:
        task_id: Task ID
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
        result = patch_json(url, token, {"percentComplete": 100}, etag)
        return result if result else {"ok": True, "taskId": task_id}
    except requests.HTTPError as e:
        if e.response.status_code == 412:  # Precondition Failed (ETag conflict)
            # Retry once
            task = get_json(url, token)
            etag = task["@odata.etag"]
            result = patch_json(url, token, {"percentComplete": 100}, etag)
            return result if result else {"ok": True, "taskId": task_id}
        raise
