"""
List Subtasks Module
List checklist items from tasks.
"""

from typing import List

from .constants import BASE_GRAPH_URL
from .graph_client import get_json


def list_subtasks(task_id: str, token: str) -> List[dict]:
    """
    List all subtasks (checklist items) for a task.

    Args:
        task_id: Task ID
        token: Access token

    Returns:
        List of subtask objects with id, title, and isChecked
    """
    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
    details = get_json(url, token)
    checklist = details.get("checklist", {})

    items = []
    for item_id, item_data in checklist.items():
        items.append({
            "id": item_id,
            "title": item_data.get("title"),
            "isChecked": item_data.get("isChecked", False)
        })

    return items
