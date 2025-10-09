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

    # Get existing checklist or initialize empty dict
    checklist = details.get("checklist", {})

    # Create a clean copy of existing items (remove @odata annotations)
    clean_checklist = {}
    for key, value in checklist.items():
        clean_checklist[key] = {
            "title": value.get("title"),
            "isChecked": value.get("isChecked", False)
        }
        # Include orderHint only if it exists
        if "orderHint" in value and value["orderHint"]:
            clean_checklist[key]["orderHint"] = value["orderHint"]

    # Generate new item ID
    item_id = str(uuid.uuid4())

    # Generate a proper orderHint based on existing items
    # For Planner API, orderHint can be: " !" or a more complex string
    # If no existing items, use " !"
    if not clean_checklist:
        order_hint = " !"
    else:
        # Get max orderHint length and add more
        existing_hints = [item.get("orderHint", " !") for item in clean_checklist.values()]
        max_hint = max(existing_hints, key=len) if existing_hints else " !"
        order_hint = max_hint + "!"

    # Add new item
    clean_checklist[item_id] = {
        "title": subtask_title,
        "isChecked": False,
        "orderHint": order_hint
    }

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

            # Rebuild clean checklist
            clean_checklist = {}
            for key, value in checklist.items():
                clean_checklist[key] = {
                    "title": value.get("title"),
                    "isChecked": value.get("isChecked", False)
                }
                if "orderHint" in value and value["orderHint"]:
                    clean_checklist[key]["orderHint"] = value["orderHint"]

            # Recalculate orderHint
            if not clean_checklist:
                order_hint = " !"
            else:
                existing_hints = [item.get("orderHint", " !") for item in clean_checklist.values()]
                max_hint = max(existing_hints, key=len) if existing_hints else " !"
                order_hint = max_hint + "!"

            # Add new item
            clean_checklist[item_id] = {
                "title": subtask_title,
                "isChecked": False,
                "orderHint": order_hint
            }
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
