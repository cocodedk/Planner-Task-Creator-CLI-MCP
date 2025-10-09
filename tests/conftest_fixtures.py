"""
Shared test fixtures - data fixtures
"""

import json


def get_mock_config_data():
    """Get standard mock config data"""
    return {
        "tenant_id": "test-tenant-id",
        "client_id": "test-client-id",
        "default_plan": "My Plan",
        "default_bucket": "To Do"
    }


def get_mock_plans_data():
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


def get_mock_buckets_data():
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


def get_mock_task_data():
    """Return mock task data"""
    return {
        "id": "task-id-123",
        "title": "Test Task",
        "planId": "plan-id-1",
        "bucketId": "bucket-id-1",
        "detailsUrl": "https://planner.cloud.microsoft/tasks/task-id-123"
    }


