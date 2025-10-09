"""
Task Creation Module
Handles creating new tasks in Microsoft Planner.
"""

from typing import Optional, Dict, Any, List

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, post_json, patch_json
from .resolution_users import resolve_users


def parse_labels(labels_csv: Optional[str]) -> Dict[str, bool]:
    """
    Parse CSV label string into Graph API category format.

    Args:
        labels_csv: Comma-separated label names like "Label1,Label3"

    Returns:
        Dictionary mapping category keys to True, e.g. {"category1": True, "category3": True}
    """
    if not labels_csv:
        return {}

    # Split and clean
    labels = [label.strip() for label in labels_csv.split(",") if label.strip()]

    categories = {}
    for label in labels:
        # Extract label number
        if label.lower().startswith("label"):
            try:
                num = label[5:]  # Extract number after "label"
                categories[f"category{num}"] = True
            except Exception:
                pass

    return categories


def build_assignments(user_ids: List[str]) -> Dict[str, dict]:
    """
    Build Graph API assignments payload structure.

    Args:
        user_ids: List of User IDs (GUIDs)

    Returns:
        Dictionary for 'assignments' field
    """
    assignments = {}
    for user_id in user_ids:
        assignments[user_id] = {
            "@odata.type": "#microsoft.graph.plannerAssignment",
            "orderHint": " !"
        }
    return assignments


def create_task(
    token: str,
    plan_id: str,
    bucket_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    labels: Optional[str] = None,
    assignee: Optional[str] = None
) -> dict:
    """
    Create a task in Microsoft Planner.

    Args:
        token: Access token
        plan_id: Plan ID
        bucket_id: Bucket ID
        title: Task title
        description: Optional task description
        due_date: Optional due date in YYYY-MM-DD format
        labels: Optional comma-separated labels
        assignee: Optional comma-separated user emails/UPNs/User IDs

    Returns:
        Dictionary with taskId, webUrl, and bucketId
    """
    # Build task payload
    payload: Dict[str, Any] = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": title
    }

    # Add optional fields
    if due_date:
        payload["dueDateTime"] = f"{due_date}T17:00:00Z"

    if labels:
        payload["appliedCategories"] = parse_labels(labels)

    if assignee:
        user_ids = resolve_users(token, assignee)
        payload["assignments"] = build_assignments(user_ids)

    # Create task
    url = f"{BASE_GRAPH_URL}/planner/tasks"
    task = post_json(url, token, payload)
    task_id = task["id"]

    # Update description if provided
    if description:
        details_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
        details = get_json(details_url, token)
        etag = details["@odata.etag"]
        patch_json(details_url, token, {"description": description}, etag)

    return {
        "taskId": task_id,
        "webUrl": task.get("detailsUrl", ""),
        "bucketId": bucket_id
    }
