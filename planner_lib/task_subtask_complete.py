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

    # Create a clean copy of checklist (remove @odata annotations)
    clean_checklist = {}
    for key, value in checklist.items():
        clean_checklist[key] = {
            "title": value.get("title"),
            "isChecked": value.get("isChecked", False)
        }
        # Include orderHint only if it exists
        if "orderHint" in value and value["orderHint"]:
            clean_checklist[key]["orderHint"] = value["orderHint"]

    # Mark the item as checked
    clean_checklist[item_id]["isChecked"] = True

    # Update with retry on ETag conflict
    try:
        patch_json(url, token, {"checklist": clean_checklist}, etag)
        return {"ok": True, "subtaskId": item_id}
    except requests.HTTPError as e:
        if e.response.status_code == 412:
            # Retry once on ETag conflict
            details = get_json(url, token)
            etag = details["@odata.etag"]
            checklist = details.get("checklist", {})

            # Find again (in case checklist changed)
            item_id = None
            for cid, item in checklist.items():
                if item.get("title", "").lower() == subtask_title.lower():
                    item_id = cid
                    break

            if not item_id:
                raise ValueError(json.dumps({
                    "code": "SubtaskNotFound",
                    "message": f"Subtask '{subtask_title}' not found after retry"
                }))

            # Rebuild clean checklist
            clean_checklist = {}
            for key, value in checklist.items():
                clean_checklist[key] = {
                    "title": value.get("title"),
                    "isChecked": value.get("isChecked", False)
                }
                if "orderHint" in value and value["orderHint"]:
                    clean_checklist[key]["orderHint"] = value["orderHint"]

            # Mark as checked
            clean_checklist[item_id]["isChecked"] = True
            patch_json(url, token, {"checklist": clean_checklist}, etag)
            return {"ok": True, "subtaskId": item_id}
        elif e.response.status_code == 400:
            # Provide more detailed error information for 400 errors
            error_detail = "Bad Request"
            try:
                error_json = e.response.json()
                error_detail = error_json.get("error", {}).get("message", error_detail)
            except:
                error_detail = e.response.text
            raise requests.HTTPError(
                f"400 Bad Request: {error_detail}",
                response=e.response
            )
        raise
