"""
Shared fixtures for user search tests
"""

from unittest.mock import MagicMock


def mock_user_search_response(users_list):
    """Create a mock response for user search"""
    return {"value": users_list}


def create_mock_user(user_id, display_name, email):
    """Create a mock user object"""
    return {
        "id": user_id,
        "displayName": display_name,
        "userPrincipalName": email,
        "mail": email
    }


def get_single_user():
    """Get a single mock user"""
    return create_mock_user(
        "user-id-1",
        "Iman Karimi",
        "iman.karimi@company.com"
    )


def get_multiple_users():
    """Get multiple mock users"""
    return [
        create_mock_user("user-id-1", "John Smith", "john.smith@company.com"),
        create_mock_user("user-id-2", "John Doe", "john.doe@company.com")
    ]


def get_three_users():
    """Get three mock users for batch tests"""
    return [
        create_mock_user("user-id-1", "User One", "user1@company.com"),
        create_mock_user("user-id-2", "User Two", "user2@company.com"),
        create_mock_user("user-id-3", "User Three", "user3@company.com")
    ]


