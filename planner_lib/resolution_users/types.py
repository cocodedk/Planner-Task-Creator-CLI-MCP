"""
Type definitions for user resolution
"""

from typing import TypedDict, List


class UserInfo(TypedDict):
    """User information from Azure AD"""
    id: str
    displayName: str
    userPrincipalName: str
    mail: str


class ResolvedUser(TypedDict):
    """Successfully resolved user"""
    input: str
    userId: str
