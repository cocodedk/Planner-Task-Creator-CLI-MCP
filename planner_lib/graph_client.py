"""
Microsoft Graph API Client Module
Handles HTTP requests to Microsoft Graph API.
"""

import time
import requests


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

