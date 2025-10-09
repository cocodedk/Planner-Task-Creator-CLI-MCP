"""
Task Management Module - Barrel Exports
Re-exports all task management operations from modular structure.
"""

from .task_operations import list_tasks, resolve_task
from .task_updates import complete_task_op, move_task_op, delete_task_op
from .task_subtasks import add_subtask, list_subtasks, complete_subtask

__all__ = [
    "list_tasks",
    "resolve_task",
    "complete_task_op",
    "move_task_op",
    "delete_task_op",
    "add_subtask",
    "list_subtasks",
    "complete_subtask",
]
