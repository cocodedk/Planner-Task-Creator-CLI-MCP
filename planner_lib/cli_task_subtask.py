"""
CLI Task Subtask Commands
Commands for managing subtasks (checklist items).
"""

import os
import json
from typing import Optional
import typer

from .constants import GUID_PATTERN
from .config import load_conf
from .auth import get_tokens
from .resolution import resolve_plan
from .task_operations import resolve_task
from .task_subtasks import add_subtask, list_subtasks, complete_subtask


def add_subtask_cmd(app: typer.Typer):
    """Add a subtask (checklist item) to a task."""
    @app.command()
    def add_subtask_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        subtask: str = typer.Option(..., "--subtask", help="Subtask title"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """Add a subtask (checklist item) to a task."""
        try:
            cfg = load_conf()
            tenant_id = cfg.get("tenant_id") or os.environ.get("TENANT_ID")
            client_id = cfg.get("client_id") or os.environ.get("CLIENT_ID")

            if not tenant_id or not client_id:
                error = {
                    "code": "ConfigError",
                    "message": "TENANT_ID and CLIENT_ID required"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            token = get_tokens(tenant_id, client_id)

            plan_id = None
            if not GUID_PATTERN.match(task):
                # Task is a title, need plan for resolution
                plan_input = plan or cfg.get("default_plan")
                if not plan_input:
                    error = {
                        "code": "ConfigError",
                        "message": "Plan required for title-based search"
                    }
                    print(json.dumps(error))
                    raise typer.Exit(2)
                plan_obj = resolve_plan(token, plan_input)
                plan_id = plan_obj["id"]
            elif plan:
                # Task is a GUID but plan was explicitly provided
                plan_obj = resolve_plan(token, plan)
                plan_id = plan_obj["id"]

            task_obj = resolve_task(token, task, plan_id)
            result = add_subtask(task_obj["id"], subtask, token)
            print(json.dumps(result, indent=2))

        except ValueError as e:
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def list_subtasks_cmd(app: typer.Typer):
    """List subtasks (checklist items) for a task."""
    @app.command()
    def list_subtasks_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """List subtasks (checklist items) for a task."""
        try:
            cfg = load_conf()
            tenant_id = cfg.get("tenant_id") or os.environ.get("TENANT_ID")
            client_id = cfg.get("client_id") or os.environ.get("CLIENT_ID")

            if not tenant_id or not client_id:
                error = {
                    "code": "ConfigError",
                    "message": "TENANT_ID and CLIENT_ID required"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            token = get_tokens(tenant_id, client_id)

            plan_id = None
            if not GUID_PATTERN.match(task):
                # Task is a title, need plan for resolution
                plan_input = plan or cfg.get("default_plan")
                if not plan_input:
                    error = {
                        "code": "ConfigError",
                        "message": "Plan required for title-based search"
                    }
                    print(json.dumps(error))
                    raise typer.Exit(2)
                plan_obj = resolve_plan(token, plan_input)
                plan_id = plan_obj["id"]
            elif plan:
                # Task is a GUID but plan was explicitly provided
                plan_obj = resolve_plan(token, plan)
                plan_id = plan_obj["id"]

            task_obj = resolve_task(token, task, plan_id)
            subtasks = list_subtasks(task_obj["id"], token)
            print(json.dumps(subtasks, indent=2))

        except ValueError as e:
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def complete_subtask_cmd(app: typer.Typer):
    """Mark a subtask (checklist item) as complete."""
    @app.command()
    def complete_subtask_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        subtask: str = typer.Option(..., "--subtask", help="Subtask title"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """Mark a subtask (checklist item) as complete."""
        try:
            cfg = load_conf()
            tenant_id = cfg.get("tenant_id") or os.environ.get("TENANT_ID")
            client_id = cfg.get("client_id") or os.environ.get("CLIENT_ID")

            if not tenant_id or not client_id:
                error = {
                    "code": "ConfigError",
                    "message": "TENANT_ID and CLIENT_ID required"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            token = get_tokens(tenant_id, client_id)

            plan_id = None
            if not GUID_PATTERN.match(task):
                # Task is a title, need plan for resolution
                plan_input = plan or cfg.get("default_plan")
                if not plan_input:
                    error = {
                        "code": "ConfigError",
                        "message": "Plan required for title-based search"
                    }
                    print(json.dumps(error))
                    raise typer.Exit(2)
                plan_obj = resolve_plan(token, plan_input)
                plan_id = plan_obj["id"]
            elif plan:
                # Task is a GUID but plan was explicitly provided
                plan_obj = resolve_plan(token, plan)
                plan_id = plan_obj["id"]

            task_obj = resolve_task(token, task, plan_id)
            result = complete_subtask(task_obj["id"], subtask, token)
            print(json.dumps(result, indent=2))

        except ValueError as e:
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)
