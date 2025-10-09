# Task Assignment Context

## Problem Statement
The CLI and MCP server currently support creating tasks with title, description, due date, and labels, but do not support assigning tasks to specific users. Task assignment is a key feature of Microsoft Planner that enables proper task delegation and accountability.

## Current State
- `planner.py add` command has an `--assignee` parameter that is flagged as "not implemented" (line 152 in `cli_commands.py`)
- The `create_task()` function in `task_creation.py` does not handle assignments
- The MCP server's `handleCreateTask` in TypeScript does not pass assignee information
- PRD acknowledges this limitation (line 613 in `0-docs/prd.md`) and suggests adding user resolution

## Microsoft Graph API Requirements

### User Resolution
To assign a task, we need the user's **Azure AD User ID** (GUID), not their email or display name. This requires:
1. Accepting user identifier input (email/UPN or User ID)
2. Resolving email/UPN to User ID via Microsoft Graph API
3. Using the User ID in the assignments payload

### Assignments Structure
The `assignments` property in Microsoft Graph API plannerTask resource:
- **Type**: `plannerAssignments` (dictionary/object)
- **Key**: Azure AD User ID (GUID)
- **Value**: Object with assignment metadata
  - `@odata.type`: "#microsoft.graph.plannerAssignment"
  - `orderHint`: Optional string for ordering (use " !" for default)
  - `assignedBy`: Read-only, set automatically by API

### API Endpoints
- **User Resolution**: `GET /users/{email}` or `GET /users?$filter=userPrincipalName eq '{email}'`
- **Task Creation with Assignment**: `POST /planner/tasks` with `assignments` in payload

## Example Graph API Payload
```json
{
  "planId": "plan-guid",
  "bucketId": "bucket-guid",
  "title": "Task Title",
  "assignments": {
    "user-guid-1": {
      "@odata.type": "#microsoft.graph.plannerAssignment",
      "orderHint": " !"
    },
    "user-guid-2": {
      "@odata.type": "#microsoft.graph.plannerAssignment",
      "orderHint": " !"
    }
  }
}
```

## Scope Considerations
- Multiple assignments: Planner supports assigning one task to multiple users
- Group context: Users must be members of the plan's owner group
- Permissions: Assigning requires appropriate permissions in the plan
