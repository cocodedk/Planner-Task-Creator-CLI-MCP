"""
Test helper utilities
Provides functions to safely access test data including IDs from environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)


def get_test_user_id_1() -> str:
    """
    Get test user ID 1 from environment or return placeholder.
    
    Returns:
        Azure AD User GUID for testing
    """
    return os.getenv("TEST_USER_ID_1", "00000000-0000-0000-0000-000000000001")


def get_test_user_id_2() -> str:
    """
    Get test user ID 2 from environment or return placeholder.
    
    Returns:
        Azure AD User GUID for testing
    """
    return os.getenv("TEST_USER_ID_2", "00000000-0000-0000-0000-000000000002")

