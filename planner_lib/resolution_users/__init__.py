"""
User Resolution Module - Barrel Exports
Handles resolving user emails/UPNs to Azure AD User IDs.
Supports partial name search for better user experience.
"""

from .search import search_users_by_name
from .resolver import resolve_user
from .batch import resolve_users
from .types import UserInfo, ResolvedUser

__all__ = [
    "search_users_by_name",
    "resolve_user",
    "resolve_users",
    "UserInfo",
    "ResolvedUser",
]
