"""
Bucket Move Module
Move all tasks from one bucket to another.
"""

from typing import List, Dict, Any

from .constants import BASE_GRAPH_URL
from .graph_client import get_json
from .task_move import move_task_op


def move_bucket_tasks_op(source_bucket_id: str, target_bucket_id: str, token: str) -> dict:
    """
    Move all tasks from source bucket to target bucket.

    Args:
        source_bucket_id: Source bucket ID
        target_bucket_id: Target bucket ID
        token: Access token

    Returns:
        Dictionary with ok, moved, failed, taskIds, errors

    Raises:
        requests.RequestException: On API errors
    """
    # Get all tasks in source bucket
    url = f"{BASE_GRAPH_URL}/planner/buckets/{source_bucket_id}/tasks"
    data = get_json(url, token)
    tasks = data.get("value", [])

    # Move each task
    moved_ids: List[str] = []
    errors: List[Dict[str, Any]] = []

    for task in tasks:
        task_id = task["id"]
        try:
            move_task_op(task_id, target_bucket_id, token)
            moved_ids.append(task_id)
        except Exception as e:
            errors.append({
                "taskId": task_id,
                "error": str(e)
            })

    return {
        "ok": True,
        "moved": len(moved_ids),
        "failed": len(errors),
        "taskIds": moved_ids,
        "errors": errors
    }
