"""
CLI Task Update Commands
Commands for updating and moving tasks.
"""

import os
import json
from typing import Optional
import typer

from .constants import GUID_PATTERN
from .config import load_conf
from .auth import get_tokens
from .resolution import resolve_plan, resolve_bucket
from .task_operations import resolve_task
from .task_updates import complete_task_op, move_task_op, delete_task_op


def complete_task_cmd(app: typer.Typer):
    """Mark a task as complete."""
    @app.command()
    def complete_task_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """Mark a task as complete."""
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
            if plan or not GUID_PATTERN.match(task):
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

            task_obj = resolve_task(token, task, plan_id)
            result = complete_task_op(task_obj["id"], token)
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


def move_task_cmd(app: typer.Typer):
    """Move a task to a different bucket."""
    @app.command()
    def move_task_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        bucket: str = typer.Option(..., "--bucket", help="Target bucket name or ID"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """Move a task to a different bucket."""
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

            # Get plan_id for bucket resolution
            plan_input = plan or cfg.get("default_plan")
            if not plan_input and not GUID_PATTERN.match(task):
                error = {
                    "code": "ConfigError",
                    "message": "Plan required for resolution"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            if plan_input:
                plan_obj = resolve_plan(token, plan_input)
                plan_id = plan_obj["id"]
            else:
                plan_id = None

            task_obj = resolve_task(token, task, plan_id)
            bucket_obj = resolve_bucket(token, plan_id, bucket)
            result = move_task_op(task_obj["id"], bucket_obj["id"], token)
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


def delete_task_cmd(app: typer.Typer):
    """Delete a task (requires --confirm flag)."""
    @app.command()
    def delete_task_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        confirm: bool = typer.Option(False, "--confirm", help="Confirm deletion"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """Delete a task (requires --confirm flag)."""
        try:
            if not confirm:
                error = {
                    "code": "ConfirmationRequired",
                    "message": "Add --confirm flag to delete task"
                }
                print(json.dumps(error))
                raise typer.Exit(1)

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
            if plan or not GUID_PATTERN.match(task):
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

            task_obj = resolve_task(token, task, plan_id)
            result = delete_task_op(task_obj["id"], token)
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
