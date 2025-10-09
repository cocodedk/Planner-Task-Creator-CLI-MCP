"""
Task Update Labels Module
Update labels on existing tasks.
"""

import requests
from typing import Optional

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, patch_json
from .task_creation import parse_labels


def update_task_labels(task_id: str, labels: Optional[str], token: str) -> dict:
    """
    Update labels on an existing task.

    Args:
        task_id: Task ID (GUID)
        labels: Comma-separated labels like "Label1,Label3" or empty string to clear
        token: Access token

    Returns:
        Updated task object

    Raises:
        requests.RequestException: On API errors
    """
    # Parse labels (empty string or None → empty dict)
    parsed_labels = parse_labels(labels) if labels else {}

    # Fetch current task for ETag
    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    task = get_json(url, token)
    etag = task["@odata.etag"]

    # Update with retry on ETag conflict
    payload = {"appliedCategories": parsed_labels}

    try:
        result = patch_json(url, token, payload, etag)
        return result if result else {"ok": True, "taskId": task_id}
    except requests.HTTPError as e:
        if e.response.status_code == 412:  # Precondition Failed (ETag conflict)
            # Retry once
            task = get_json(url, token)
            etag = task["@odata.etag"]
            result = patch_json(url, token, payload, etag)
            return result if result else {"ok": True, "taskId": task_id}
        raise
