"""
Task Comments Module
Handles reading and adding comments to Planner tasks via conversation threads.
"""

import json
import logging
from typing import List, Optional

import requests

from .constants import BASE_GRAPH_URL
from .graph_client import get_json, post_json

logger = logging.getLogger(__name__)


def _get_validated_plan(plan_id: str, token: str) -> dict:
    """
    Retrieve and validate a plan.

    Args:
        plan_id: Plan ID (GUID)
        token: Access token

    Returns:
        Plan dictionary

    Raises:
        ValueError: JSON-encoded error if plan cannot be retrieved or is invalid
    """
    plan_url = f"{BASE_GRAPH_URL}/planner/plans/{plan_id}"
    try:
        plan = get_json(plan_url, token)
        # Validate plan response
        if not isinstance(plan, dict):
            logger.error(f"Plan retrieval returned invalid response format for plan_id={plan_id}, plan_url={plan_url}")
            raise ValueError(json.dumps({
                "code": "InvalidPlanResponse",
                "message": f"Plan {plan_id} returned invalid response format"
            }))
        if not plan:
            logger.error(f"Plan retrieval returned empty response for plan_id={plan_id}, plan_url={plan_url}")
            raise ValueError(json.dumps({
                "code": "PlanNotFound",
                "message": f"Plan {plan_id} not found or returned empty response"
            }))
    except ValueError:
        # Re-raise ValueError exceptions (already controlled)
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to retrieve plan: plan_id={plan_id}, plan_url={plan_url}, error={error_msg}")
        # Handle specific error cases
        if "404" in error_msg or "NotFound" in error_msg:
            raise ValueError(json.dumps({
                "code": "PlanNotFound",
                "message": f"Plan {plan_id} not found"
            }))
        # Handle network/HTTP/parsing errors
        raise ValueError(json.dumps({
            "code": "PlanAccessError",
            "message": f"Could not access plan {plan_id}: {error_msg}"
        }))
    return plan


def get_task_comments(task_id: str, plan_id: str, token: str) -> List[dict]:
    """
    Fetch comments from task's conversation thread.

    Args:
        task_id: Task ID (GUID)
        plan_id: Plan ID (to get group ID)
        token: Access token

    Returns:
        List of comment objects with author, content, and createdDateTime

    Raises:
        ValueError: If task or plan not found, or if comments cannot be accessed
    """
    # Get task to find conversationThreadId
    task_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    try:
        task = get_json(task_url, token)
    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response else None
        error_msg = str(e)
        logger.error(f"HTTP error fetching task {task_id}: {error_msg} (status: {status_code})")
        error_response = {
            "error": f"Failed to fetch task: {error_msg}",
            "status": status_code
        }
        raise ValueError(json.dumps(error_response))
    except requests.RequestException as e:
        error_msg = str(e)
        logger.error(f"Request error fetching task {task_id}: {error_msg}")
        error_response = {
            "error": f"Network error fetching task: {error_msg}",
            "status": None
        }
        raise ValueError(json.dumps(error_response))
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Unexpected error fetching task {task_id}: {error_msg}")
        error_response = {
            "error": f"Unexpected error fetching task: {error_msg}",
            "status": None
        }
        raise ValueError(json.dumps(error_response))
    conversation_thread_id = task.get("conversationThreadId")

    if not conversation_thread_id:
        # Task has no comments thread yet
        return []

    # Get plan to find group ID
    plan = _get_validated_plan(plan_id, token)

    group_id = plan.get("owner")

    if not group_id:
        raise ValueError(json.dumps({
            "code": "NoGroupOwner",
            "message": f"Plan {plan_id} has no owner group"
        }))

    # Get conversation thread posts
    try:
        posts_url = f"{BASE_GRAPH_URL}/groups/{group_id}/threads/{conversation_thread_id}/posts"
        posts_data = get_json(posts_url, token)
        posts = posts_data.get("value", [])

        comments = []
        for post in posts:
            # Extract author info
            from_field = post.get("from", {})
            author = from_field.get("emailAddress", {})

            # Extract body content
            body = post.get("body", {})
            content = body.get("content", "")

            comments.append({
                "id": post.get("id"),
                "author": {
                    "name": author.get("name", ""),
                    "email": author.get("address", "")
                },
                "content": content,
                "createdDateTime": post.get("createdDateTime", "")
            })

        return comments
    except Exception as e:
        # If thread doesn't exist or access denied, return empty list
        error_msg = str(e)
        if "404" in error_msg or "NotFound" in error_msg:
            return []
        raise ValueError(json.dumps({
            "code": "CommentsAccessError",
            "message": f"Could not access comments: {error_msg}"
        }))


def add_task_comment(task_id: str, plan_id: str, comment: str, token: str) -> dict:
    """
    Add a comment to a task's conversation thread.

    Args:
        task_id: Task ID (GUID)
        plan_id: Plan ID (to get group ID)
        comment: Comment text to add
        token: Access token

    Returns:
        Dictionary with success status and comment ID

    Raises:
        ValueError: If task or plan not found, or if comment cannot be added
    """
    if not comment or not comment.strip():
        raise ValueError(json.dumps({
            "code": "InvalidComment",
            "message": "Comment cannot be empty"
        }))

    # Get task to find or create conversationThreadId
    task_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    try:
        task = get_json(task_url, token)
        # Validate task response
        if not isinstance(task, dict):
            raise ValueError(json.dumps({
                "code": "InvalidTaskResponse",
                "message": f"Task {task_id} returned invalid response format"
            }))
        # Ensure task contains expected structure (at minimum, should have an id)
        if "id" not in task:
            raise ValueError(json.dumps({
                "code": "InvalidTaskData",
                "message": f"Task {task_id} response missing required fields"
            }))
    except ValueError:
        # Re-raise ValueError exceptions (already controlled)
        raise
    except Exception as e:
        error_msg = str(e)
        # Handle specific error cases
        if "404" in error_msg or "NotFound" in error_msg:
            raise ValueError(json.dumps({
                "code": "TaskNotFound",
                "message": f"Task {task_id} not found"
            }))
        # Handle network/HTTP/parsing errors
        raise ValueError(json.dumps({
            "code": "TaskAccessError",
            "message": f"Could not access task {task_id}: {error_msg}"
        }))

    conversation_thread_id = task.get("conversationThreadId")

    # Get plan to find group ID
    plan = _get_validated_plan(plan_id, token)

    group_id = plan.get("owner")

    if not group_id:
        raise ValueError(json.dumps({
            "code": "NoGroupOwner",
            "message": f"Plan {plan_id} has no owner group"
        }))

    # If no thread exists, we need to create one
    # For now, we'll try to reply to existing thread or create via task details
    if not conversation_thread_id:
        # Try to get/create thread via task details
        # Note: Microsoft Graph API may require creating the thread first
        # This is a limitation - we can only add comments if a thread already exists
        raise ValueError(json.dumps({
            "code": "NoThread",
            "message": "Task has no conversation thread. Comments can only be added to tasks that already have a thread (created via Planner UI)."
        }))

    # Reply to existing thread
    try:
        reply_url = f"{BASE_GRAPH_URL}/groups/{group_id}/threads/{conversation_thread_id}/reply"
        payload = {
            "post": {
                "body": {
                    "contentType": "text",
                    "content": comment
                }
            }
        }
        result = post_json(reply_url, token, payload)
        return {
            "ok": True,
            "taskId": task_id,
            "commentId": result.get("id", "")
        }
    except Exception as e:
        error_msg = str(e)
        raise ValueError(json.dumps({
            "code": "CommentAddError",
            "message": f"Could not add comment: {error_msg}"
        }))
