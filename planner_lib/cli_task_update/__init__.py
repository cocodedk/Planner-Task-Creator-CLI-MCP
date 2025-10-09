"""
CLI Task Update Commands - Barrel Exports
Re-exports all task update commands from modular structure.
"""

from .complete import complete_task_cmd
from .move import move_task_cmd
from .delete import delete_task_cmd
from .update_labels import update_task_labels_cmd

__all__ = [
    "complete_task_cmd",
    "move_task_cmd",
    "delete_task_cmd",
    "update_task_labels_cmd",
]
