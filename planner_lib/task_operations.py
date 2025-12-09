"""
Task Operations Module
Core task operations: list and resolve tasks.
"""

import json
from typing import Optional, List

from .constants import BASE_GRAPH_URL, GUID_PATTERN
from .graph_client import get_json
from .resolution_utils import case_insensitive_match


def list_tasks(
    token: str,
    plan_id: Optional[str] = None,
    bucket_id: Optional[str] = None,
    incomplete_only: bool = False
) -> List[dict]:
    """
    List tasks from a plan or bucket.

    Args:
        token: Access token
        plan_id: Plan ID (required if bucket_id not provided)
        bucket_id: Bucket ID (takes precedence over plan_id)
        incomplete_only: Filter to show only incomplete tasks

    Returns:
        List of task objects with description included

    Raises:
        ValueError: If neither plan_id nor bucket_id provided
    """
    if bucket_id:
        url = f"{BASE_GRAPH_URL}/planner/buckets/{bucket_id}/tasks"
    elif plan_id:
        url = f"{BASE_GRAPH_URL}/planner/plans/{plan_id}/tasks"
    else:
        raise ValueError("plan_id or bucket_id required")

    data = get_json(url, token)
    tasks = data.get("value", [])

    if incomplete_only:
        tasks = [t for t in tasks if t.get("percentComplete", 0) < 100]

    # Fetch descriptions for all tasks
    for task in tasks:
        task_id = task.get("id")
        if task_id:
            try:
                details_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
                details = get_json(details_url, token)
                task["description"] = details.get("description", "")
            except Exception:
                # If details fetch fails, set empty description
                task["description"] = ""

    return tasks


def resolve_task(token: str, task: str, plan_id: Optional[str] = None) -> dict:
    """
    Resolve task identifier (ID or title) to task object.

    Args:
        token: Access token
        task: Task ID (GUID) or task title
        plan_id: Plan ID (required for title search)

    Returns:
        Task object with full details including description

    Raises:
        ValueError: With JSON error if task not found or ambiguous
    """
    # GUID → fetch directly
    if GUID_PATTERN.match(task):
        url = f"{BASE_GRAPH_URL}/planner/tasks/{task}"
        task_obj = get_json(url, token)
        # Fetch description
        task_id = task_obj.get("id")
        if task_id:
            try:
                details_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
                details = get_json(details_url, token)
                task_obj["description"] = details.get("description", "")
            except Exception:
                task_obj["description"] = ""
        return task_obj

    # Title → search
    if not plan_id:
        raise ValueError(json.dumps({
            "code": "ConfigError",
            "message": "plan_id required for title-based task search"
        }))

    tasks = list_tasks(token, plan_id=plan_id)
    matches = case_insensitive_match(tasks, "title", task)

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        candidates = [{"id": t["id"], "title": t["title"], "bucketId": t.get("bucketId", "")}
                     for t in matches]
        error = {
            "code": "AmbiguousTask",
            "message": f"Multiple tasks match '{task}'",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))
    else:
        candidates = [{"id": t["id"], "title": t["title"]} for t in tasks[:5]]
        error = {
            "code": "TaskNotFound",
            "message": f"Task '{task}' not found",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))


def get_task_details(task_id: str, token: str) -> dict:
    """
    Fetch task details by task ID.

    Args:
        task_id: Task GUID
        token: Access token

    Returns:
        Full task object with all properties including description

    Raises:
        ValueError: If task_id invalid format or task not found
    """
    if not GUID_PATTERN.match(task_id):
        raise ValueError(json.dumps({
            "code": "InvalidTaskId",
            "message": f"Invalid task ID format: {task_id}"
        }))

    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    task_obj = get_json(url, token)

    # Fetch description
    try:
        details_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
        details = get_json(details_url, token)
        task_obj["description"] = details.get("description", "")
    except Exception:
        task_obj["description"] = ""

    return task_obj


def find_task_by_title(title: str, plan_id: str, token: str) -> dict:
    """
    Find task by title within a plan.

    Args:
        title: Task title (case-insensitive)
        plan_id: Plan ID to search within
        token: Access token

    Returns:
        Task object if single match found (includes description)

    Raises:
        ValueError: With candidates if ambiguous or not found
    """
    tasks = list_tasks(token, plan_id=plan_id)
    matches = case_insensitive_match(tasks, "title", title)

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        candidates = [{"id": t["id"], "title": t["title"], "bucketId": t.get("bucketId", "")}
                     for t in matches]
        raise ValueError(json.dumps({
            "code": "AmbiguousTask",
            "message": f"Multiple tasks match '{title}'",
            "candidates": candidates
        }))
    else:
        candidates = [{"id": t["id"], "title": t["title"]} for t in tasks[:5]]
        raise ValueError(json.dumps({
            "code": "TaskNotFound",
            "message": f"Task '{title}' not found",
            "candidates": candidates
        }))
