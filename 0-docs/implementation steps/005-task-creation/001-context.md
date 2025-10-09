# Task Creation Module Context

**Purpose**: Create Microsoft Planner tasks with all supported fields via Graph API.

**Scope**: Handle task creation, description updates, and label parsing.

**Key Requirements**:
- Create task with planId, bucketId, title (required)
- Set due date in ISO format with time zone
- Parse CSV labels into Graph API format
- Handle description via details endpoint with ETag
- Return task ID and web URL for CLI output
