"""
CLI Update Task Labels Command
Update labels on existing tasks.
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
from ..task_update_labels import update_task_labels


def update_task_labels_cmd(app: typer.Typer):
    """Update labels on an existing task."""
    @app.command()
    def update_task_labels_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        labels: str = typer.Option("", "--labels", help="Comma-separated labels (e.g., Label1,Label3) or empty to clear"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """Update labels on an existing task."""
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
            result = update_task_labels(task_obj["id"], labels, token)
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
