"""
Microsoft Planner CLI Library
Modular components for Microsoft Planner task management.
"""

from .config import get_config_path, load_conf, save_conf
from .auth import get_cache_path, get_tokens
from .graph_client import auth_headers, get_json, post_json, patch_json
from .resolution import (
    case_insensitive_match,
    list_user_plans,
    list_plan_buckets,
    resolve_plan,
    resolve_bucket
)
from .task_creation import parse_labels, create_task
from .task_management import (
    list_tasks,
    resolve_task,
    complete_task_op,
    move_task_op,
    add_subtask,
    list_subtasks,
    complete_subtask,
    delete_task_op
)

__all__ = [
    # Config
    "get_config_path",
    "load_conf",
    "save_conf",
    # Auth
    "get_cache_path",
    "get_tokens",
    # Graph Client
    "auth_headers",
    "get_json",
    "post_json",
    "patch_json",
    # Resolution
    "case_insensitive_match",
    "list_user_plans",
    "list_plan_buckets",
    "resolve_plan",
    "resolve_bucket",
    # Task Creation
    "parse_labels",
    "create_task",
    # Task Management
    "list_tasks",
    "resolve_task",
    "complete_task_op",
    "move_task_op",
    "add_subtask",
    "list_subtasks",
    "complete_subtask",
    "delete_task_op",
]
