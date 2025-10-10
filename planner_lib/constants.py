"""
Constants for Microsoft Planner CLI
"""

import re

BASE_GRAPH_URL = "https://graph.microsoft.com/v1.0"
REQUIRED_SCOPES = ["Tasks.ReadWrite"]

# Pattern to match both standard GUIDs and Microsoft Planner IDs
# Standard GUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# Planner ID: 28-character base64url string (e.g., HxHB4Ts0WUa2IWMS_o1B8JgAOlVA)
GUID_PATTERN = re.compile(
    r'^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|[A-Za-z0-9_-]{20,40})$'
)
