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

    # Create a clean copy of existing items with @odata.type annotation
    # Note: We regenerate orderHints to avoid API-generated formats that may be invalid
    clean_checklist = {}
    for key, value in checklist.items():
        clean_checklist[key] = {
            "@odata.type": "#microsoft.graph.plannerChecklistItem",
            "title": value.get("title"),
            "isChecked": value.get("isChecked", False)
        }
        # Do NOT include orderHint from existing items as API may generate invalid formats
        # We'll generate new hints based on position

    # Generate new item ID
    item_id = str(uuid.uuid4())

    # Generate a proper orderHint based on existing items
    # For Planner API, orderHint format rules:
    # - Must contain at least one space and end with exclamation point
    # - Number of exclamation points must be >= number of spaces
    # - Valid: " !", " !!", " !!!", etc.
    if not clean_checklist:
        order_hint = " !"
    else:
        # Use equal spaces and exclamation points for simplicity
        num_items = len(clean_checklist)
        order_hint = " " * (num_items + 1) + "!" * (num_items + 1)

    # Add new item with @odata.type annotation
    clean_checklist[item_id] = {
        "@odata.type": "#microsoft.graph.plannerChecklistItem",
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

            # Rebuild clean checklist with @odata.type annotation
            clean_checklist = {}
            for key, value in checklist.items():
                clean_checklist[key] = {
                    "@odata.type": "#microsoft.graph.plannerChecklistItem",
                    "title": value.get("title"),
                    "isChecked": value.get("isChecked", False)
                }
                # Do NOT include orderHint from existing items

            # Recalculate orderHint
            if not clean_checklist:
                order_hint = " !"
            else:
                num_items = len(clean_checklist)
                order_hint = " " * (num_items + 1) + "!" * (num_items + 1)

            # Add new item with @odata.type annotation
            clean_checklist[item_id] = {
                "@odata.type": "#microsoft.graph.plannerChecklistItem",
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
