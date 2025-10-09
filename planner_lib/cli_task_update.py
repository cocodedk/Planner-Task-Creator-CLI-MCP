"""
CLI Task Update Commands - re-export from modular structure
"""
from .cli_task_update import (
    complete_task_cmd,
    move_task_cmd,
    delete_task_cmd,
    update_task_labels_cmd,
)

__all__ = [
    "complete_task_cmd",
    "move_task_cmd",
    "delete_task_cmd",
    "update_task_labels_cmd",
]
