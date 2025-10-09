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
        List of task objects

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

    return tasks


def resolve_task(token: str, task: str, plan_id: Optional[str] = None) -> dict:
    """
    Resolve task identifier (ID or title) to task object.

    Args:
        token: Access token
        task: Task ID (GUID) or task title
        plan_id: Plan ID (required for title search)

    Returns:
        Task object with full details

    Raises:
        ValueError: With JSON error if task not found or ambiguous
    """
    # GUID → fetch directly
    if GUID_PATTERN.match(task):
        url = f"{BASE_GRAPH_URL}/planner/tasks/{task}"
        return get_json(url, token)

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
