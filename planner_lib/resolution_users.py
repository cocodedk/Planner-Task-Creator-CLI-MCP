"""
User Resolution Module - re-export from modular structure
"""
from .resolution_users import (
    search_users_by_name,
    resolve_user,
    resolve_users,
    UserInfo,
    ResolvedUser,
)

__all__ = [
    "search_users_by_name",
    "resolve_user",
    "resolve_users",
    "UserInfo",
    "ResolvedUser",
]
