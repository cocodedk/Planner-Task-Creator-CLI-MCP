"""
CLI Delete Task Command
Delete tasks with confirmation.
"""

import os
import json
from typing import Optional
import typer

from ..constants import GUID_PATTERN
from ..config import load_conf
from ..auth import get_tokens
from ..resolution import resolve_plan
from ..task_operations import resolve_task
from ..task_updates import delete_task_op


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
