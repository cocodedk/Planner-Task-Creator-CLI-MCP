"""
CLI Bucket Commands Module
Implements Typer CLI commands for bucket management.
"""

import os
import json
from typing import Optional
import typer
from rich.console import Console

from .config import load_conf
from .auth import get_tokens
from .resolution import resolve_plan, resolve_bucket
from .bucket_create import create_bucket_op
from .bucket_delete import delete_bucket_op
from .bucket_update import update_bucket_op
from .bucket_move import move_bucket_tasks_op

console = Console()


def create_bucket_cmd(app: typer.Typer):
    """Create a new bucket in a plan."""
    @app.command("create-bucket")
    def create_bucket(
        name: str = typer.Option(..., "--name", help="Bucket name"),
        plan: str = typer.Option(..., "--plan", help="Plan name or ID")
    ):
        """Create a new bucket in a plan."""
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
            result = create_bucket_op(plan_obj["id"], name, token)
            print(json.dumps(result, indent=2))

        except ValueError as e:
            # Resolution error with JSON
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def delete_bucket_cmd(app: typer.Typer):
    """Delete a bucket from a plan."""
    @app.command("delete-bucket")
    def delete_bucket(
        bucket: str = typer.Option(..., "--bucket", help="Bucket name or ID"),
        plan: str = typer.Option(..., "--plan", help="Plan name or ID")
    ):
        """Delete a bucket from a plan."""
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
            bucket_obj = resolve_bucket(token, plan_obj["id"], bucket)
            result = delete_bucket_op(bucket_obj["id"], token)
            print(json.dumps(result, indent=2))

        except ValueError as e:
            # Resolution error with JSON
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def rename_bucket_cmd(app: typer.Typer):
    """Rename a bucket."""
    @app.command("rename-bucket")
    def rename_bucket(
        bucket: str = typer.Option(..., "--bucket", help="Bucket name or ID"),
        new_name: str = typer.Option(..., "--new-name", help="New bucket name"),
        plan: str = typer.Option(..., "--plan", help="Plan name or ID")
    ):
        """Rename a bucket."""
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
            bucket_obj = resolve_bucket(token, plan_obj["id"], bucket)
            result = update_bucket_op(bucket_obj["id"], new_name, token)
            print(json.dumps(result, indent=2))

        except ValueError as e:
            # Resolution error with JSON
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def move_bucket_tasks_cmd(app: typer.Typer):
    """Move all tasks from one bucket to another."""
    @app.command("move-bucket-tasks")
    def move_bucket_tasks(
        source: str = typer.Option(..., "--source", help="Source bucket name or ID"),
        target: str = typer.Option(..., "--target", help="Target bucket name or ID"),
        plan: str = typer.Option(..., "--plan", help="Plan name or ID")
    ):
        """Move all tasks from source bucket to target bucket."""
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
            source_obj = resolve_bucket(token, plan_obj["id"], source)
            target_obj = resolve_bucket(token, plan_obj["id"], target)
            result = move_bucket_tasks_op(source_obj["id"], target_obj["id"], token)
            print(json.dumps(result, indent=2))

        except ValueError as e:
            # Resolution error with JSON
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def register_bucket_commands(app: typer.Typer):
    """Register all bucket CLI commands with the Typer app."""
    create_bucket_cmd(app)
    delete_bucket_cmd(app)
    rename_bucket_cmd(app)
    move_bucket_tasks_cmd(app)
