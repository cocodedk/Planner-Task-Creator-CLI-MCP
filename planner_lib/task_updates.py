"""
Task Updates Module - Barrel Exports
Re-exports all task update operations from modular structure.
"""

from .task_complete import complete_task_op
from .task_move import move_task_op
from .task_delete import delete_task_op

__all__ = [
    "complete_task_op",
    "move_task_op",
    "delete_task_op",
]
