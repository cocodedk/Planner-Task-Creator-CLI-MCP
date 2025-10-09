# Task Assignment Investigation Summary

## Investigation Scope
How to assign tasks to users in Microsoft Planner using Microsoft Graph API within the context of this CLI/MCP project.

## Key Findings

### 1. Microsoft Graph API Assignments Property
- **Resource**: `plannerTask`
- **Property**: `assignments` (type: `plannerAssignments`)
- **Structure**: Object/dictionary with User IDs as keys
- **Format**:
  ```json
  {
    "assignments": {
      "{user-guid}": {
        "@odata.type": "#microsoft.graph.plannerAssignment",
        "orderHint": " !"
      }
    }
  }
  ```

### 2. User Identification Requirements
- Microsoft Graph requires **Azure AD User ID (GUID)**, not email directly in assignments
- User resolution needed: Email/UPN → User ID
- API endpoint: `GET /users/{email}` or `GET /users/{userId}`
- Response contains `id` field with User ID

### 3. Current Codebase State
- Infrastructure exists: `--assignee` parameter in CLI (not implemented)
- Pattern established: Similar resolution modules for plans and buckets
- PRD acknowledges: Task assignment is a recognized gap (line 613)
- Architecture supports: Modular resolution pattern fits naturally

### 4. Multiple Assignments
- Planner supports assigning one task to multiple users
- Common use case in team collaboration
- Implementation: Add multiple User IDs as keys in assignments object

### 5. Security and Permissions
- Users must be members of the plan's owner group (Microsoft 365 Group)
- Graph API handles permission validation
- Invalid users return 404 or permission errors

### 6. Best Practices Observed
- **User Input**: Accept email (user-friendly) or User ID (power users)
- **Resolution Pattern**: Similar to plan/bucket resolution (GUID check → API call)
- **Error Handling**: Fail fast on invalid users before task creation
- **CSV Format**: Align with existing labels parameter (comma-separated)

## Implementation Impact

### Files to Create
- `planner_lib/resolution_users.py` - User resolution module
- `tests/test_resolution_users.py` - Unit tests

### Files to Modify
- `planner_lib/task_creation.py` - Add assignments support
- `planner_lib/cli_commands.py` - Enable assignee parameter
- `src/server/handlers-core.ts` - Pass assignee to CLI
- `src/server/tools.ts` - Add assignee to tool schema
- `tests/test_task_creation.py` - Add assignment tests

### Complexity Assessment
- **Low-Medium**: Follows established patterns
- **Risk**: User resolution API calls (network, permissions)
- **Dependencies**: None beyond existing Graph API client

## References
- Microsoft Graph API: User resource type
- Microsoft Graph API: plannerTask resource type
- Existing resolution modules: `resolution_plans.py`, `resolution_buckets.py`
- PRD section 15 (line 613): Acknowledged gap

## Recommendations
1. Implement user resolution following bucket/plan pattern
2. Support multiple assignees from start (minor added complexity)
3. Use default orderHint to simplify implementation
4. Add comprehensive error messages for user resolution failures
5. Document email format requirements (UPN) in tool descriptions
