"""
Constants for Microsoft Planner CLI
"""

import re

BASE_GRAPH_URL = "https://graph.microsoft.com/v1.0"
REQUIRED_SCOPES = ["Tasks.ReadWrite"]
GUID_PATTERN = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
