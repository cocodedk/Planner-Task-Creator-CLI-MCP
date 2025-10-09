# Task Assignment Decisions

## User Resolution Strategy
**Decision**: Accept comma-separated email addresses or User IDs, resolve emails to User IDs.

**Rationale**:
- Users typically know email addresses, not Azure AD GUIDs
- Support for User IDs provides power-user shortcut
- Comma-separated format aligns with existing labels parameter pattern

**Alternative Considered**: Accept only emails
- **Rejected**: Less flexible for automation and power users

## Resolution Module Location
**Decision**: Create new `resolution_users.py` module following existing patterns.

**Rationale**:
- Matches existing architecture with `resolution_plans.py` and `resolution_buckets.py`
- Separates concerns and maintains modularity
- Follows established naming conventions

## API Endpoint Choice
**Decision**: Use `GET /users/{email}` for single user, handle errors gracefully.

**Rationale**:
- Most direct API call
- UPN/email serves as valid user identifier in Graph API
- Error handling will catch invalid users before task creation

**Alternative Considered**: `GET /users?$filter=userPrincipalName eq '{email}'`
- **Trade-off**: More verbose but more explicit; rejected for simplicity

## Multiple Assignees Support
**Decision**: Support multiple assignees from initial implementation.

**Rationale**:
- Planner natively supports multi-assignment
- Minor additional complexity (loop over users)
- Common use case in team environments

## Assignment Ordering
**Decision**: Use default `orderHint: " !"` for all assignments.

**Rationale**:
- Order is rarely important for assignees
- Simplifies implementation
- Can be enhanced later if needed

## Error Handling
**Decision**: Fail fast on invalid users during resolution phase.

**Rationale**:
- Prevents partial task creation with missing assignments
- Clear error messages before API calls
- Aligns with existing resolution error patterns (plans, buckets)

## CLI Flag Name
**Decision**: Keep existing `--assignee` parameter name.

**Rationale**:
- Already defined in codebase
- Clear and conventional
- Supports both singular and plural via comma-separated values

## MCP Parameter Name
**Decision**: Use `assignee` (singular) in MCP schema.

**Rationale**:
- Maintains consistency with CLI
- Schema description can clarify comma-separated format
- Aligns with existing MCP parameter patterns
