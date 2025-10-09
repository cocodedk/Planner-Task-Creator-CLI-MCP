"""
Task Delete Module
Delete tasks from planner.
"""

import requests

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, auth_headers


def delete_task_op(task_id: str, token: str) -> dict:
    """
    Delete a task.

    Args:
        task_id: Task ID
        token: Access token

    Returns:
        Success dict

    Raises:
        requests.RequestException: On API errors
    """
    # Fetch current task for ETag
    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    task = get_json(url, token)
    etag = task["@odata.etag"]

    # Delete with ETag
    headers = auth_headers(token)
    headers["If-Match"] = etag

    response = requests.delete(url, headers=headers)
    response.raise_for_status()

    return {"ok": True, "taskId": task_id}
