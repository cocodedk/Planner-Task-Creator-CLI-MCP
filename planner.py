#!/usr/bin/env python3
"""
Microsoft Planner Task Creator CLI
A command-line tool for creating and managing Microsoft Planner tasks.
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from typing import Optional, List, Dict, Any

import msal
import requests
import typer
from rich.console import Console

# Initialize CLI app and console
app = typer.Typer(help="Microsoft Planner Task Creator CLI")
console = Console()

# Constants
BASE_GRAPH_URL = "https://graph.microsoft.com/v1.0"
REQUIRED_SCOPES = ["Tasks.ReadWrite"]
GUID_PATTERN = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


# =============================================================================
# MODULE 003: Configuration Management
# =============================================================================

def get_config_path() -> Path:
    """Get configuration file path from environment or default."""
    config_path = os.environ.get("PLANNER_CONFIG_PATH")
    if config_path:
        return Path(config_path).expanduser()
    return Path.home() / ".planner-cli" / "config.json"


def load_conf() -> dict:
    """Load configuration from file, return empty dict if not found."""
    config_path = get_config_path()
    try:
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_conf(cfg: dict) -> None:
    """Save configuration to file with proper permissions."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(cfg, f, indent=2)

    # Set file permissions to 0600 (owner read/write only)
    os.chmod(config_path, 0o600)


# =============================================================================
# MODULE 001: Authentication
# =============================================================================

def get_cache_path() -> Path:
    """Get token cache file path."""
    return Path.home() / ".planner-cli" / "msal_cache.bin"


def get_tokens(tenant_id: str, client_id: str) -> str:
    """
    Acquire access token using device code flow with caching.

    Args:
        tenant_id: Azure AD tenant ID
        client_id: Azure AD app registration client ID

    Returns:
        Valid access token string

    Raises:
        RuntimeError: If authentication fails
    """
    if not tenant_id or not client_id:
        raise RuntimeError("TENANT_ID and CLIENT_ID are required")

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    cache_path = get_cache_path()

    # Initialize token cache
    cache = msal.SerializableTokenCache()
    if cache_path.exists():
        with open(cache_path, 'r') as f:
            cache.deserialize(f.read())

    # Create MSAL app
    app_client = msal.PublicClientApplication(
        client_id=client_id,
        authority=authority,
        token_cache=cache
    )

    # Try to acquire token silently from cache
    accounts = app_client.get_accounts()
    if accounts:
        result = app_client.acquire_token_silent(REQUIRED_SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    # No cached token, initiate device code flow
    flow = app_client.initiate_device_flow(scopes=REQUIRED_SCOPES)
    if "user_code" not in flow:
        raise RuntimeError("Failed to initiate device code flow")

    # Display device code instructions
    console.print(f"\n[bold cyan]Authentication Required[/bold cyan]")
    console.print(f"Please visit: [bold]{flow['verification_uri']}[/bold]")
    console.print(f"Enter code: [bold yellow]{flow['user_code']}[/bold yellow]\n")

    # Poll for token
    result = app_client.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        error_desc = result.get("error_description", "Unknown error")
        raise RuntimeError(f"Authentication failed: {error_desc}")

    # Save cache
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, 'w') as f:
        f.write(cache.serialize())
    os.chmod(cache_path, 0o600)

    return result["access_token"]


# =============================================================================
# MODULE 002: Graph API Client
# =============================================================================

def auth_headers(token: str) -> dict:
    """Create authentication headers for Graph API requests."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def get_json(url: str, token: str) -> dict:
    """
    Make GET request to Graph API with retry on rate limit.

    Args:
        url: Full URL to request
        token: Access token

    Returns:
        Parsed JSON response

    Raises:
        requests.RequestException: On network or HTTP errors
    """
    headers = auth_headers(token)
    response = requests.get(url, headers=headers)

    # Handle rate limiting
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", "2"))
        time.sleep(retry_after)
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json()


def post_json(url: str, token: str, payload: dict) -> dict:
    """
    Make POST request to Graph API with retry on rate limit.

    Args:
        url: Full URL to request
        token: Access token
        payload: JSON payload

    Returns:
        Parsed JSON response

    Raises:
        requests.RequestException: On network or HTTP errors
    """
    headers = auth_headers(token)
    response = requests.post(url, headers=headers, json=payload)

    # Handle rate limiting
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", "2"))
        time.sleep(retry_after)
        response = requests.post(url, headers=headers, json=payload)

    response.raise_for_status()
    return response.json()


def patch_json(url: str, token: str, payload: dict, etag: str) -> dict:
    """
    Make PATCH request to Graph API with ETag.

    Args:
        url: Full URL to request
        token: Access token
        payload: JSON payload
        etag: ETag for optimistic concurrency

    Returns:
        Parsed JSON response or empty dict

    Raises:
        requests.RequestException: On network or HTTP errors
    """
    headers = auth_headers(token)
    headers["If-Match"] = etag

    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()

    if response.content:
        return response.json()
    return {}


# =============================================================================
# MODULE 004: Resolution
# =============================================================================

def case_insensitive_match(items: List[dict], key: str, value: str) -> List[dict]:
    """Filter list of dictionaries by case-insensitive key value match."""
    value_lower = value.lower()
    return [item for item in items if item.get(key, "").lower() == value_lower]


def list_user_plans(token: str) -> List[dict]:
    """
    List all plans accessible to the user with group names.

    Args:
        token: Access token

    Returns:
        List of plan objects with optional groupName field
    """
    url = f"{BASE_GRAPH_URL}/me/planner/plans"
    data = get_json(url, token)
    plans = data.get("value", [])

    # Augment with group names
    for plan in plans:
        owner_id = plan.get("owner")
        if owner_id:
            try:
                group_url = f"{BASE_GRAPH_URL}/groups/{owner_id}"
                group_data = get_json(group_url, token)
                plan["groupName"] = group_data.get("displayName", "")
            except Exception:
                pass

    return plans


def list_plan_buckets(plan_id: str, token: str) -> List[dict]:
    """
    List all buckets in a specific plan.

    Args:
        plan_id: Plan ID
        token: Access token

    Returns:
        List of bucket objects
    """
    url = f"{BASE_GRAPH_URL}/planner/plans/{plan_id}/buckets"
    data = get_json(url, token)
    return data.get("value", [])


def resolve_plan(token: str, plan: str) -> dict:
    """
    Resolve plan name or ID to plan object.

    Args:
        token: Access token
        plan: Plan name or ID

    Returns:
        Plan object with 'id' field

    Raises:
        ValueError: With JSON error object if not found or ambiguous
    """
    # Check if input is a GUID
    if GUID_PATTERN.match(plan):
        return {"id": plan}

    # Fetch all plans
    plans = list_user_plans(token)

    # Find case-insensitive matches
    matches = case_insensitive_match(plans, "title", plan)

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        candidates = [{"id": p["id"], "title": p["title"], "groupName": p.get("groupName", "")}
                     for p in matches]
        error = {
            "code": "Ambiguous",
            "message": f"Multiple plans match '{plan}'",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))
    else:
        candidates = [{"id": p["id"], "title": p["title"], "groupName": p.get("groupName", "")}
                     for p in plans]
        error = {
            "code": "NotFound",
            "message": f"Plan '{plan}' not found",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))


def resolve_bucket(token: str, plan_id: str, bucket: str) -> dict:
    """
    Resolve bucket name or ID to bucket object.

    Args:
        token: Access token
        plan_id: Plan ID
        bucket: Bucket name or ID

    Returns:
        Bucket object with 'id' field

    Raises:
        ValueError: With JSON error object if not found or ambiguous
    """
    # Check if input is a GUID
    if GUID_PATTERN.match(bucket):
        return {"id": bucket}

    # Fetch all buckets
    buckets = list_plan_buckets(plan_id, token)

    # Find case-insensitive matches
    matches = case_insensitive_match(buckets, "name", bucket)

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        candidates = [{"id": b["id"], "name": b["name"]} for b in matches]
        error = {
            "code": "Ambiguous",
            "message": f"Multiple buckets match '{bucket}'",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))
    else:
        candidates = [{"id": b["id"], "name": b["name"]} for b in buckets]
        error = {
            "code": "NotFound",
            "message": f"Bucket '{bucket}' not found",
            "candidates": candidates
        }
        raise ValueError(json.dumps(error))


# =============================================================================
# MODULE 005: Task Creation
# =============================================================================

def parse_labels(labels_csv: Optional[str]) -> Dict[str, bool]:
    """
    Parse CSV label string into Graph API category format.

    Args:
        labels_csv: Comma-separated label names like "Label1,Label3"

    Returns:
        Dictionary mapping category keys to True, e.g. {"category1": True, "category3": True}
    """
    if not labels_csv:
        return {}

    # Split and clean
    labels = [label.strip() for label in labels_csv.split(",") if label.strip()]

    categories = {}
    for label in labels:
        # Extract label number
        if label.lower().startswith("label"):
            try:
                num = label[5:]  # Extract number after "label"
                categories[f"category{num}"] = True
            except Exception:
                pass

    return categories


def create_task(
    token: str,
    plan_id: str,
    bucket_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    labels: Optional[str] = None
) -> dict:
    """
    Create a task in Microsoft Planner.

    Args:
        token: Access token
        plan_id: Plan ID
        bucket_id: Bucket ID
        title: Task title
        description: Optional task description
        due_date: Optional due date in YYYY-MM-DD format
        labels: Optional comma-separated labels

    Returns:
        Dictionary with taskId, webUrl, and bucketId
    """
    # Build task payload
    payload: Dict[str, Any] = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": title
    }

    # Add optional fields
    if due_date:
        payload["dueDateTime"] = f"{due_date}T17:00:00Z"

    if labels:
        payload["appliedCategories"] = parse_labels(labels)

    # Create task
    url = f"{BASE_GRAPH_URL}/planner/tasks"
    task = post_json(url, token, payload)
    task_id = task["id"]

    # Update description if provided
    if description:
        details_url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}/details"
        details = get_json(details_url, token)
        etag = details["@odata.etag"]
        patch_json(details_url, token, {"description": description}, etag)

    return {
        "taskId": task_id,
        "webUrl": task.get("detailsUrl", ""),
        "bucketId": bucket_id
    }


# =============================================================================
# MODULE 006: CLI Commands
# =============================================================================

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


@app.command()
def add(
    title: str = typer.Option(..., "--title", help="Task title"),
    plan: Optional[str] = typer.Option(None, "--plan", help="Plan name or ID"),
    bucket: Optional[str] = typer.Option(None, "--bucket", help="Bucket name or ID"),
    desc: Optional[str] = typer.Option(None, "--desc", help="Task description"),
    due: Optional[str] = typer.Option(None, "--due", help="Due date (YYYY-MM-DD)"),
    assignee: Optional[str] = typer.Option(None, "--assignee", help="Assignee email (not implemented)"),
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
            labels=labels
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


if __name__ == "__main__":
    app()
