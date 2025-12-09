"""
Constants for Microsoft Planner CLI
"""

import re

BASE_GRAPH_URL = "https://graph.microsoft.com/v1.0"
# Required scopes for Planner operations
# Tasks.ReadWrite: Required for all task operations
# Group.Read.All: Required for reading task comments (conversation threads)
# Group.ReadWrite.All: Required for adding task comments (conversation threads)
REQUIRED_SCOPES = [
    "Tasks.ReadWrite",
    "Group.Read.All",  # For reading task comments
    "Group.ReadWrite.All",  # For adding task comments
]

# Pattern to match both standard GUIDs and Microsoft Planner IDs
# Standard GUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# Planner ID: 28-character base64url string (e.g., HxHB4Ts0WUa2IWMS_o1B8JgAOlVA)
GUID_PATTERN = re.compile(
    r'^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|[A-Za-z0-9_-]{20,40})$'
)
