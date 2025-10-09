"""
CLI Commands Module
Implements core Typer CLI commands for the planner application.
"""

import os
import json
from typing import Optional
import typer
from rich.console import Console

from .config import load_conf, save_conf
from .auth import get_tokens
from .resolution import resolve_plan, resolve_bucket, list_user_plans, list_plan_buckets
from .task_creation import create_task

console = Console()


def init_auth_cmd(app: typer.Typer):
    """Initialize authentication with Microsoft."""
    @app.command()
    def init_auth():
        """Initialize authentication with Microsoft."""
        try:
            cfg = load_conf()
            tenant_id = cfg.get("tenant_id") or os.environ.get("TENANT_ID")
            client_id = cfg.get("client_id") or os.environ.get("CLIENT_ID")

            if not tenant_id or not client_id:
                error = {
                    "code": "ConfigError",
                    "message": "TENANT_ID and CLIENT_ID required in environment or config file"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            get_tokens(tenant_id, client_id)
            console.print("[green]✓ Authentication successful![/green]")

        except Exception as e:
            error = {
                "code": "AuthError",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def set_defaults_cmd(app: typer.Typer):
    """Set default plan and bucket for task creation."""
    @app.command()
    def set_defaults(
        plan: str = typer.Option(..., "--plan", help="Default plan name or ID"),
        bucket: str = typer.Option(..., "--bucket", help="Default bucket name or ID")
    ):
        """Set default plan and bucket for task creation."""
        try:
            cfg = load_conf()
            cfg["default_plan"] = plan
            cfg["default_bucket"] = bucket
            save_conf(cfg)
            console.print(f"[green]✓ Defaults saved:[/green] plan='{plan}', bucket='{bucket}'")

        except Exception as e:
            error = {
                "code": "ConfigError",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def list_plans_cmd(app: typer.Typer):
    """List all available plans."""
    @app.command()
    def list_plans():
        """List all available plans."""
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
            plans = list_user_plans(token)
            print(json.dumps(plans, indent=2))

        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def list_buckets_cmd(app: typer.Typer):
    """List all buckets in a plan."""
    @app.command()
    def list_buckets(
        plan: str = typer.Option(..., "--plan", help="Plan name or ID")
    ):
        """List all buckets in a plan."""
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
            buckets = list_plan_buckets(plan_obj["id"], token)
            print(json.dumps(buckets, indent=2))

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


def add_task_cmd(app: typer.Typer):
    """Create a new task in Microsoft Planner."""
    @app.command()
    def add(
        title: str = typer.Option(..., "--title", help="Task title"),
        plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID"),
        bucket: Optional[str] = typer.Option(None, "--bucket", help="Bucket name or ID"),
        desc: Optional[str] = typer.Option(None, "--desc", help="Task description"),
        due: Optional[str] = typer.Option(None, "--due", help="Due date (YYYY-MM-DD)"),
        assignee: Optional[str] = typer.Option(None, "--assignee", help="Comma-separated user emails or User IDs"),
        labels: Optional[str] = typer.Option(None, "--labels", help="Comma-separated labels (e.g., Label1,Label3)"),
        verbose: bool = typer.Option(False, "--verbose", help="Verbose output")
    ):
        """Create a new task in Microsoft Planner."""
        try:
            cfg = load_conf()

            # Resolve configuration
            tenant_id = cfg.get("tenant_id") or os.environ.get("TENANT_ID")
            client_id = cfg.get("client_id") or os.environ.get("CLIENT_ID")
            plan_input = plan or os.environ.get("PLANNER_DEFAULT_PLAN") or cfg.get("default_plan")
            bucket_input = bucket or os.environ.get("PLANNER_DEFAULT_BUCKET") or cfg.get("default_bucket")

            # Validate required config
            if not tenant_id or not client_id:
                error = {
                    "code": "ConfigError",
                    "message": "TENANT_ID and CLIENT_ID required"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            if not plan_input or not bucket_input:
                error = {
                    "code": "ConfigError",
                    "message": "Plan and bucket required (via flags, env vars, or config defaults)"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            # Authenticate
            token = get_tokens(tenant_id, client_id)

            # Resolve plan and bucket
            plan_obj = resolve_plan(token, plan_input)
            bucket_obj = resolve_bucket(token, plan_obj["id"], bucket_input)

            # Create task
            result = create_task(
                token=token,
                plan_id=plan_obj["id"],
                bucket_id=bucket_obj["id"],
                title=title,
                description=desc,
                due_date=due,
                labels=labels,
                assignee=assignee
            )

            # Output result
            print(json.dumps(result, indent=2))

            if verbose:
                console.print(f"[green]✓ Task created:[/green] {title}")
                console.print(f"  Task ID: {result['taskId']}")
                if result['webUrl']:
                    console.print(f"  URL: {result['webUrl']}")

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


def register_all_commands(app: typer.Typer):
    """Register all core CLI commands with the Typer app."""
    init_auth_cmd(app)
    set_defaults_cmd(app)
    list_plans_cmd(app)
    list_buckets_cmd(app)
    add_task_cmd(app)
