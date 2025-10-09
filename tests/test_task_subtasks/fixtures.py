"""
Shared fixtures for subtask tests
"""

import pytest


@pytest.fixture
def mock_task_details():
    """Return mock task details with checklist"""
    return {
        "id": "details-id-123",
        "checklist": {
            "subtask-id-1": {
                "title": "Write tests",
                "isChecked": False,
                "orderHint": " !"
            },
            "subtask-id-2": {
                "title": "Update docs",
                "isChecked": True,
                "orderHint": " !!"
            }
        },
        "@odata.etag": "W/\"etag123\""
    }


@pytest.fixture
def mock_empty_task_details():
    """Return mock task details without checklist"""
    return {
        "id": "details-id-456",
        "@odata.etag": "W/\"etag456\""
    }
