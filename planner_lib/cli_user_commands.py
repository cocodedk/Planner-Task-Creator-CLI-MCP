"""
CLI Commands for User Operations
Handles user search and lookup commands.
"""

import json
import os
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .auth import get_tokens
from .config import load_conf
from .resolution_users import search_users_by_name, resolve_user

console = Console()


def search_user_cmd(app: typer.Typer):
    """Search for users by display name."""
    @app.command()
    def search(
        query: str = typer.Argument(..., help="Search term (name or partial name)"),
        verbose: bool = typer.Option(False, "--verbose", help="Verbose output")
    ):
        """Search for users in Azure AD by display name."""
        try:
            cfg = load_conf()

            # Get authentication config
            tenant_id = cfg.get("tenant_id") or os.environ.get("TENANT_ID")
            client_id = cfg.get("client_id") or os.environ.get("CLIENT_ID")

            if not tenant_id or not client_id:
                error = {
                    "code": "ConfigError",
                    "message": "TENANT_ID and CLIENT_ID required"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            # Authenticate
            token = get_tokens(tenant_id, client_id)

            # Search for users
            results = search_users_by_name(token, query)

            if len(results) == 0:
                if verbose:
                    console.print(f"[yellow]No users found matching '{query}'[/yellow]")

                output = {
                    "count": 0,
                    "users": []
                }
                print(json.dumps(output, indent=2))
                return

            # Format results
            users = []
            for user in results:
                user_data = {
                    "id": user.get("id", ""),
                    "displayName": user.get("displayName", "Unknown"),
                    "email": user.get("mail") or user.get("userPrincipalName", ""),
                    "userPrincipalName": user.get("userPrincipalName", "")
                }
                users.append(user_data)

            output = {
                "count": len(users),
                "users": users
            }

            # JSON output
            print(json.dumps(output, indent=2))

            # Rich table output (verbose mode)
            if verbose:
                console.print(f"\n[green]Found {len(users)} user(s) matching '{query}':[/green]\n")

                table = Table(show_header=True, header_style="bold cyan")
                table.add_column("Display Name", style="white")
                table.add_column("Email", style="yellow")
                table.add_column("User ID", style="dim")

                for user in users:
                    table.add_row(
                        user["displayName"],
                        user["email"],
                        user["id"]
                    )

                console.print(table)
                console.print("\n[dim]Tip: Use the email or User ID with --assignee flag[/dim]")

        except ValueError as e:
            # Error with JSON output
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def lookup_user_cmd(app: typer.Typer):
    """Resolve a user identifier to full user details."""
    @app.command()
    def lookup(
        user: str = typer.Argument(..., help="User email, UPN, ID, or partial name"),
        no_search: bool = typer.Option(False, "--no-search", help="Disable partial name search"),
        verbose: bool = typer.Option(False, "--verbose", help="Verbose output")
    ):
        """Resolve user identifier to Azure AD User ID."""
        try:
            cfg = load_conf()

            # Get authentication config
            tenant_id = cfg.get("tenant_id") or os.environ.get("TENANT_ID")
            client_id = cfg.get("client_id") or os.environ.get("CLIENT_ID")

            if not tenant_id or not client_id:
                error = {
                    "code": "ConfigError",
                    "message": "TENANT_ID and CLIENT_ID required"
                }
                print(json.dumps(error))
                raise typer.Exit(2)

            # Authenticate
            token = get_tokens(tenant_id, client_id)

            # Resolve user
            enable_search = not no_search
            user_id = resolve_user(token, user, enable_search=enable_search)

            # Get full user details
            from .constants import BASE_GRAPH_URL
            from .graph_client import get_json

            url = f"{BASE_GRAPH_URL}/users/{user_id}?$select=id,displayName,userPrincipalName,mail,jobTitle,department"
            user_data = get_json(url, token)

            # Format output
            output = {
                "id": user_data.get("id", ""),
                "displayName": user_data.get("displayName", "Unknown"),
                "email": user_data.get("mail") or user_data.get("userPrincipalName", ""),
                "userPrincipalName": user_data.get("userPrincipalName", ""),
                "jobTitle": user_data.get("jobTitle", ""),
                "department": user_data.get("department", "")
            }

            # JSON output
            print(json.dumps(output, indent=2))

            # Verbose output
            if verbose:
                console.print(f"\n[green]✓ User found:[/green]")
                console.print(f"  Name: {output['displayName']}")
                console.print(f"  Email: {output['email']}")
                console.print(f"  User ID: {output['id']}")
                if output['jobTitle']:
                    console.print(f"  Title: {output['jobTitle']}")
                if output['department']:
                    console.print(f"  Department: {output['department']}")

        except ValueError as e:
            # Error with JSON output (includes AmbiguousUser errors)
            print(str(e))
            raise typer.Exit(2)
        except Exception as e:
            error = {
                "code": "Error",
                "message": str(e)
            }
            print(json.dumps(error))
            raise typer.Exit(2)


def register_user_commands(app: typer.Typer):
    """Register all user-related commands."""
    # Create a sub-app for user commands
    user_app = typer.Typer(help="User search and lookup commands")

    # Register commands
    search_user_cmd(user_app)
    lookup_user_cmd(user_app)

    # Add sub-app to main app
    app.add_typer(user_app, name="user")
