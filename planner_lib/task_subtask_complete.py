"""
Complete Subtask Module
Mark checklist items as complete.
"""

import json
import requests

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, patch_json


def complete_subtask(task_id: str, subtask_title: str, token: str) -> dict:
    """
    Mark a subtask (checklist item) as complete.

    Args:
        task_id: Task ID
        subtask_title: Subtask title to find and complete
        token: Access token

    Returns:
        Success dict

    Raises:
        ValueError: If subtask not found
        requests.RequestException: On API errors
    """
    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
    details = get_json(url, token)
    etag = details["@odata.etag"]
    checklist = details.get("checklist", {})

    # Find by title (case-insensitive)
    item_id = None
    for cid, item in checklist.items():
        if item.get("title", "").lower() == subtask_title.lower():
            item_id = cid
            break

    if not item_id:
        raise ValueError(json.dumps({
            "code": "SubtaskNotFound",
            "message": f"Subtask '{subtask_title}' not found"
        }))

    checklist[item_id]["isChecked"] = True

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
            # Find again (in case checklist changed)
            for cid, item in checklist.items():
                if item.get("title", "").lower() == subtask_title.lower():
                    item_id = cid
                    break
            if item_id:
                checklist[item_id]["isChecked"] = True
                patch_json(url, token, {"checklist": checklist}, etag)
            return {"ok": True, "subtaskId": item_id}
        raise
