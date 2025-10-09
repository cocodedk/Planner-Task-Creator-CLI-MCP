"""
Tests for authentication module (001-authentication)
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, mock_open
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from planner import get_tokens, get_cache_path


def test_get_tokens_device_flow(mocker, mock_msal_app, tmp_path):
    """Test device code flow authentication"""
    # Mock file operations
    mocker.patch("pathlib.Path.exists", return_value=False)
    mock_file = mocker.patch("builtins.open", mock_open())
    mocker.patch("os.chmod")

    # Mock cache path
    mocker.patch("planner.get_cache_path", return_value=tmp_path / "cache.bin")

    # Call get_tokens
    token = get_tokens("test-tenant", "test-client")

    # Verify token returned
    assert token == "mock_access_token"

    # Verify MSAL app was created correctly
    import msal
    msal.PublicClientApplication.assert_called_once()

    # Verify device flow was initiated
    mock_msal_app.initiate_device_flow.assert_called_once()
    mock_msal_app.acquire_token_by_device_flow.assert_called_once()


def test_get_tokens_from_cache(mocker, mock_msal_app, tmp_path):
    """Test token retrieval from cache"""
    # Mock cached token
    mock_msal_app.get_accounts.return_value = [{"username": "test@example.com"}]
    mock_msal_app.acquire_token_silent.return_value = {
        "access_token": "cached_token"
    }

    # Mock file operations
    mocker.patch("pathlib.Path.exists", return_value=True)
    mock_file = mocker.patch("builtins.open", mock_open(read_data="cached_data"))
    mocker.patch("planner.get_cache_path", return_value=tmp_path / "cache.bin")

    # Call get_tokens
    token = get_tokens("test-tenant", "test-client")

    # Verify cached token returned
    assert token == "cached_token"

    # Verify silent acquisition was attempted
    mock_msal_app.acquire_token_silent.assert_called_once()


def test_get_tokens_missing_credentials():
    """Test error handling for missing credentials"""
    with pytest.raises(RuntimeError, match="TENANT_ID and CLIENT_ID are required"):
        get_tokens("", "")


def test_get_tokens_auth_failure(mocker, mock_msal_app, tmp_path):
    """Test error handling for authentication failure"""
    # Mock failed authentication
    mock_msal_app.acquire_token_by_device_flow.return_value = {
        "error": "invalid_grant",
        "error_description": "User cancelled authentication"
    }

    # Mock file operations
    mocker.patch("pathlib.Path.exists", return_value=False)
    mocker.patch("planner.get_cache_path", return_value=tmp_path / "cache.bin")
    mock_file = mocker.patch("builtins.open", mock_open())

    with pytest.raises(RuntimeError, match="Authentication failed"):
        get_tokens("test-tenant", "test-client")


def test_cache_path():
    """Test cache path generation"""
    path = get_cache_path()
    assert path.name == "msal_cache.bin"
    assert ".planner-cli" in str(path)
