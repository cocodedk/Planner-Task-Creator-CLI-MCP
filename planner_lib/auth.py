"""
Authentication Module
Handles Microsoft authentication with device code flow and token caching.
"""

import os
from pathlib import Path
import msal
from rich.console import Console

from .constants import REQUIRED_SCOPES

console = Console()


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

