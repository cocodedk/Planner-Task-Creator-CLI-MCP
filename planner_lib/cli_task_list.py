"""
CLI Task List Commands
Commands for listing and finding tasks.
"""

import os
import json
from typing import Optional
import typer

from .constants import GUID_PATTERN
from .config import load_conf
from .auth import get_tokens
from .resolution import resolve_plan, resolve_bucket
from .task_operations import list_tasks, resolve_task


def list_tasks_cmd(app: typer.Typer):
    """List tasks in a plan or bucket."""
    @app.command()
    def list_tasks_cmd(
        plan: str = typer.Option(..., "--plan", help="Plan name or ID"),
        bucket: Optional[str] = typer.Option(None, "--bucket", help="Bucket name or ID"),
        incomplete: bool = typer.Option(False, "--incomplete", help="Show only incomplete tasks")
    ):
        """List tasks in a plan or bucket."""
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
            plan_obj = resolve_plan(token, plan)

            bucket_id = None
            if bucket:
                bucket_obj = resolve_bucket(token, plan_obj["id"], bucket)
                bucket_id = bucket_obj["id"]

            tasks = list_tasks(token, plan_id=plan_obj["id"], bucket_id=bucket_id, incomplete_only=incomplete)
            print(json.dumps(tasks, indent=2))

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


def find_task_cmd(app: typer.Typer):
    """Find a task by ID or title."""
    @app.command()
    def find_task_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID")
    ):
        """Find a task by ID or title."""
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
            print(json.dumps(task_obj, indent=2))

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
