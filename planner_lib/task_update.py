"""
Task Update Module
Update various properties on existing tasks (title, description, labels).
"""

import requests
from typing import Optional

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, patch_json
from .task_creation import parse_labels


def update_task_op(
    task_id: str,
    token: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    labels: Optional[str] = None
) -> dict:
    """
    Update properties on an existing task.

    Args:
        task_id: Task ID (GUID)
        title: New task title (optional)
        description: New task description (optional)
        labels: Comma-separated labels like "Label1,Label3" or empty string to clear (optional)
        token: Access token

    Returns:
        Updated task object

    Raises:
        requests.RequestException: On API errors
    """
    # Fetch current task for ETag and details
    task_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    task = get_json(task_url, token)
    etag = task["@odata.etag"]

    # Build payload for task properties (title)
    task_payload = {}
    if title is not None:
        task_payload["title"] = title

    # Build payload for labels
    if labels is not None:
        parsed_labels = parse_labels(labels) if labels else {}
        task_payload["appliedCategories"] = parsed_labels

    # Update task if there are task-level changes
    if task_payload:
        try:
            result = patch_json(task_url, token, task_payload, etag)
        except requests.HTTPError as e:
            if e.response.status_code == 412:  # Precondition Failed (ETag conflict)
                # Retry once
                task = get_json(task_url, token)
                etag = task["@odata.etag"]
                result = patch_json(task_url, token, task_payload, etag)
            else:
                raise

    # Update description if provided (separate endpoint)
    if description is not None:
        details_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
        details = get_json(details_url, token)
        details_etag = details["@odata.etag"]

        try:
            patch_json(details_url, token, {"description": description}, details_etag)
        except requests.HTTPError as e:
            if e.response.status_code == 412:
                # Retry once
                details = get_json(details_url, token)
                details_etag = details["@odata.etag"]
                patch_json(details_url, token, {"description": description}, details_etag)
            else:
                raise

    return {"ok": True, "taskId": task_id}
