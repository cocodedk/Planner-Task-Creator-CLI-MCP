"""
Add Subtask Module
Add checklist items to tasks.
"""

import uuid
import requests

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, patch_json


def add_subtask(task_id: str, subtask_title: str, token: str) -> dict:
    """
    Add a subtask (checklist item) to a task.

    Args:
        task_id: Task ID
        subtask_title: Subtask title
        token: Access token

    Returns:
        Success dict with subtask ID

    Raises:
        requests.RequestException: On API errors
    """
    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
    details = get_json(url, token)
    etag = details["@odata.etag"]

    checklist = details.get("checklist", {})
    item_id = str(uuid.uuid4())
    checklist[item_id] = {
        "title": subtask_title,
        "isChecked": False,
        "orderHint": " !"
    }

    # Update with retry on ETag conflict
    try:
        patch_json(url, token, {"checklist": checklist}, etag)
        return {"ok": True, "subtaskId": item_id}
    except requests.HTTPError as e:
        if e.response.status_code == 412:
            # Retry once
            details = get_json(url, token)
            etag = details["@odata.etag"]
            checklist = details.get("checklist", {})
            checklist[item_id] = {
                "title": subtask_title,
                "isChecked": False,
                "orderHint": " !"
            }
            patch_json(url, token, {"checklist": checklist}, etag)
            return {"ok": True, "subtaskId": item_id}
        raise
