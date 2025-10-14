"""
Task operations tests module
"""

from .test_list_tasks import TestListTasks
from .test_resolve_task import TestResolveTask
from .test_find_enhancements import TestGetTaskDetails, TestFindTaskByTitle, TestBackwardCompatibility

__all__ = [
    "TestListTasks",
    "TestResolveTask",
    "TestGetTaskDetails",
    "TestFindTaskByTitle",
    "TestBackwardCompatibility"
]
