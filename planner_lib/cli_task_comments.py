"""
CLI Task Comments Commands
Commands for reading and adding task comments.
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
from .task_comments import get_task_comments, add_task_comment


def list_comments_cmd(app: typer.Typer):
    """List comments on a task."""
    @app.command()
    def list_comments_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        plan: str = typer.Option(..., "--plan", help="Plan name or ID")
    ):
        """List all comments on a task."""
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

            # Resolve plan
            plan_obj = resolve_plan(token, plan)
            plan_id = plan_obj["id"]

            # Resolve task
            task_obj = resolve_task(token, task, plan_id)
            task_id = task_obj["id"]

            # Get comments
            comments = get_task_comments(task_id, plan_id, token)
            print(json.dumps(comments, indent=2))

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


def add_comment_cmd(app: typer.Typer):
    """Add a comment to a task."""
    @app.command()
    def add_comment_cmd(
        task: str = typer.Option(..., "--task", help="Task ID or title"),
        comment: str = typer.Option(..., "--comment", help="Comment text"),
        plan: str = typer.Option(..., "--plan", help="Plan name or ID")
    ):
        """Add a comment to a task."""
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

            # Resolve plan
            plan_obj = resolve_plan(token, plan)
            plan_id = plan_obj["id"]

            # Resolve task
            task_obj = resolve_task(token, task, plan_id)
            task_id = task_obj["id"]

            # Add comment
            result = add_task_comment(task_id, plan_id, comment, token)
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
