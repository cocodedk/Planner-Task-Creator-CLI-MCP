"""
Shared test fixtures and mocks for planner CLI tests
"""

import json
import pytest
from unittest.mock import MagicMock, Mock
from pathlib import Path


@pytest.fixture
def mock_config_dir(tmp_path):
    """Create a temporary config directory"""
    config_dir = tmp_path / ".planner-cli"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def mock_config_file(mock_config_dir):
    """Create a mock config file"""
    config_file = mock_config_dir / "config.json"
    config_data = {
        "tenant_id": "test-tenant-id",
        "client_id": "test-client-id",
        "default_plan": "My Plan",
        "default_bucket": "To Do"
    }
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture
def mock_token():
    """Return a mock access token"""
    return "mock_access_token_12345"


@pytest.fixture
def mock_plans():
    """Return mock plans data"""
    return [
        {
            "id": "plan-id-1",
            "title": "My Plan",
            "owner": "group-id-1",
            "groupName": "My Team"
        },
        {
            "id": "plan-id-2",
            "title": "Another Plan",
            "owner": "group-id-2",
            "groupName": "Another Team"
        }
    ]


@pytest.fixture
def mock_buckets():
    """Return mock buckets data"""
    return [
        {
            "id": "bucket-id-1",
            "name": "To Do",
            "planId": "plan-id-1"
        },
        {
            "id": "bucket-id-2",
            "name": "In Progress",
            "planId": "plan-id-1"
        },
        {
            "id": "bucket-id-3",
            "name": "Done",
            "planId": "plan-id-1"
        }
    ]


@pytest.fixture
def mock_task():
    """Return mock task data"""
    return {
        "id": "task-id-123",
        "title": "Test Task",
        "planId": "plan-id-1",
        "bucketId": "bucket-id-1",
        "detailsUrl": "https://planner.cloud.microsoft/tasks/task-id-123"
    }


@pytest.fixture
def mock_msal_app(mocker):
    """Mock MSAL PublicClientApplication"""
    mock_app = MagicMock()
    mock_app.get_accounts.return_value = []
    mock_app.initiate_device_flow.return_value = {
        "user_code": "TEST1234",
        "verification_uri": "https://microsoft.com/devicelogin",
        "expires_in": 900
    }
    mock_app.acquire_token_by_device_flow.return_value = {
        "access_token": "mock_access_token"
    }

    mocker.patch("msal.PublicClientApplication", return_value=mock_app)
    mocker.patch("msal.SerializableTokenCache")

    return mock_app


@pytest.fixture
def mock_requests(mocker):
    """Mock requests library"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"value": []}
    mock_response.raise_for_status.return_value = None
    mock_response.content = b"{}"
    mock_response.headers = {}

    mock_get = mocker.patch("requests.get", return_value=mock_response)
    mock_post = mocker.patch("requests.post", return_value=mock_response)
    mock_patch = mocker.patch("requests.patch", return_value=mock_response)

    return {
        "get": mock_get,
        "post": mock_post,
        "patch": mock_patch,
        "response": mock_response
    }
