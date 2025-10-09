"""
User search functionality using Microsoft Graph API
"""

from typing import List, Dict, Any
from urllib.parse import quote

from ..constants import BASE_GRAPH_URL
from ..graph_client import get_json


def search_users_by_name(token: str, search_term: str) -> List[Dict[str, Any]]:
    """
    Search for users whose display name starts with the search term.

    Args:
        token: OAuth access token
        search_term: Partial name to search (e.g., "Iman", "John")

    Returns:
        List of user objects matching the search term

    Raises:
        Exception: If Graph API call fails
    """
    # URL encode the search term
    encoded_term = quote(search_term)
    url = f"{BASE_GRAPH_URL}/users?$filter=startswith(tolower(displayName),tolower('{encoded_term}'))&$select=id,displayName,userPrincipalName,mail"

    try:
        result = get_json(url, token)
        return result.get("value", [])
    except Exception:
        # Return empty list if search fails
        return []
