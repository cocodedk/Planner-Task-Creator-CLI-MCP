"""
CLI Complete Task Command
Mark tasks as complete.
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
from ..task_updates import complete_task_op


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
