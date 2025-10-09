# Task Assignment Implementation Specification

## New Module: `resolution_users.py`

### Function: `resolve_user(token: str, user_identifier: str) -> str`

**Purpose**: Resolve user email/UPN or User ID to Azure AD User ID (GUID).

**Parameters**:
- `token`: OAuth access token
- `user_identifier`: Email/UPN or User ID (GUID)

**Returns**: User ID (GUID) as string

**Logic**:
1. Check if input matches GUID pattern
   - If yes, return as-is (assume valid User ID)
2. Attempt to resolve as email/UPN:
   - `GET {BASE_GRAPH_URL}/users/{user_identifier}`
   - Extract `id` field from response
3. Handle errors:
   - 404: User not found → raise `ValueError` with JSON error
   - Other HTTP errors → propagate

**Error Format**:
```json
{
  "code": "UserNotFound",
  "message": "User '{user_identifier}' not found or not accessible"
}
```

### Function: `resolve_users(token: str, assignee_csv: str) -> List[str]`

**Purpose**: Parse comma-separated user identifiers and resolve all to User IDs.

**Parameters**:
- `token`: OAuth access token
- `assignee_csv`: Comma-separated emails/UPNs/User IDs

**Returns**: List of User IDs (GUIDs)

**Logic**:
1. Split by comma, strip whitespace
2. Filter empty strings
3. For each identifier, call `resolve_user(token, identifier)`
4. Return list of resolved User IDs

**Error Handling**: First resolution error propagates immediately

## Modified Module: `task_creation.py`

### Function: `build_assignments(user_ids: List[str]) -> Dict[str, dict]`

**Purpose**: Build Graph API assignments payload structure.

**Parameters**:
- `user_ids`: List of User IDs (GUIDs)

**Returns**: Dictionary for `assignments` field

**Logic**:
```python
assignments = {}
for user_id in user_ids:
    assignments[user_id] = {
        "@odata.type": "#microsoft.graph.plannerAssignment",
        "orderHint": " !"
    }
return assignments
```

### Updated Function: `create_task(..., assignee: Optional[str] = None) -> dict`

**New Parameter**: `assignee` - Comma-separated user emails/UPNs/User IDs

**Modified Logic**:
1. Build base payload (existing code)
2. **NEW**: If assignee provided:
   ```python
   from .resolution_users import resolve_users
   user_ids = resolve_users(token, assignee)
   payload["assignments"] = build_assignments(user_ids)
   ```
3. POST to `/planner/tasks` (existing code)
4. Update description if provided (existing code)
5. Return result (existing code)

## Modified Module: `cli_commands.py`

### Updated Command: `add_task_cmd`

**Changes**:
1. Remove placeholder comment on line 152
2. Pass `assignee` parameter to `create_task()`:
   ```python
   result = create_task(
       token=token,
       plan_id=plan_obj["id"],
       bucket_id=bucket_obj["id"],
       title=title,
       description=desc,
       due_date=due,
       labels=labels,
       assignee=assignee  # NEW
   )
   ```

## Modified Module: `src/server/handlers-core.ts`

### Updated Function: `handleCreateTask`

**Changes**:
1. Add `assignee?: string` to args interface
2. Pass to CLI:
   ```typescript
   if (args.assignee) {
     cliArgs.push("--assignee", args.assignee);
   }
   ```

## Modified Module: `src/server/tools.ts`

### Updated Tool: `planner_createTask`

**Changes**:
1. Add `assignee` to `properties`:
   ```typescript
   assignee: {
     type: "string",
     description: "Comma-separated user emails or User IDs (e.g., user1@example.com,user2@example.com)"
   }
   ```

## Testing Requirements

### Unit Tests (`tests/test_resolution_users.py`)
- Test GUID passthrough
- Test email resolution (requires mock)
- Test CSV parsing
- Test error handling (user not found)

### Integration Tests (`tests/test_task_creation.py`)
- Test task creation with single assignee
- Test task creation with multiple assignees
- Test task creation without assignee (backward compatibility)
- Test error propagation for invalid user

### Manual Tests
- CLI: `planner.py add --title "Test" --plan "MyPlan" --bucket "MyBucket" --assignee "user@example.com"`
- MCP: Use MCP client to create task with assignee
- Verify in Planner web UI that task is assigned correctly

## Implementation Order
1. Create `resolution_users.py` with both functions
2. Add `build_assignments()` to `task_creation.py`
3. Update `create_task()` in `task_creation.py`
4. Update CLI command in `cli_commands.py`
5. Update TypeScript handlers and tools
6. Build TypeScript: `npm run build`
7. Write and run tests
8. Manual verification
