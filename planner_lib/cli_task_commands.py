"""
Task Management CLI Commands - Barrel Exports
Re-exports all task CLI commands from modular structure.
"""

import typer
from .cli_task_list import list_tasks_cmd, find_task_cmd
from .cli_task_update import complete_task_cmd, move_task_cmd, delete_task_cmd
from .cli_task_subtask import add_subtask_cmd, list_subtasks_cmd, complete_subtask_cmd


def register_task_commands(app: typer.Typer):
    """Register all task management CLI commands."""
    list_tasks_cmd(app)
    find_task_cmd(app)
    complete_task_cmd(app)
    move_task_cmd(app)
    add_subtask_cmd(app)
    list_subtasks_cmd(app)
    complete_subtask_cmd(app)
    delete_task_cmd(app)
