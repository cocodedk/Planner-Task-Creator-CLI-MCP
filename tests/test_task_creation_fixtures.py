"""
Fixtures for task creation tests
"""


def get_mock_task_response():
    """Get a standard mock task response"""
    return {
        "id": "task-id-123",
        "title": "Test Task",
        "planId": "plan-id-1",
        "bucketId": "bucket-id-1",
        "detailsUrl": "https://planner.cloud.microsoft/tasks/task-id-123"
    }


def get_mock_task_details_response():
    """Get a standard mock task details response"""
    return {
        "@odata.etag": "W/\"test-etag\"",
        "description": ""
    }


