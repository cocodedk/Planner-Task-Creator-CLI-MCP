# Task Assignment Feature

## User Resolution Module

**Purpose**: Resolve user identifiers (email, display name, GUID) to Azure AD User IDs for task assignment

**Key Components**:
- `planner_lib/resolution_users/` - Modular user resolution package
  - `resolver.py` - Single user resolution with fallback strategies
  - `search.py` - Case-insensitive user search by display name
  - `batch.py` - Batch user resolution with comprehensive error reporting
  - `utils.py` - Error formatting and helper functions
  - `types.py` - Type definitions for user data

**Resolution Strategy**:
1. If input is a GUID → return directly
2. Try exact match by email/UPN (requires `User.Read.All` permission)
3. Try partial name search (case-insensitive with `tolower()` filter)
4. Report detailed errors with suggestions for ambiguous matches

**Required Permissions**:
- `User.Read.All` or `User.ReadBasic.All` (delegated, requires admin consent)
- Without these permissions, email/name-based user lookup will fail with 401 Unauthorized
- Users can still be assigned using their Azure AD User ID (GUID) directly

**Error Handling**:
- `UserNotFound` - No users match the identifier
- `AmbiguousUser` - Multiple users match, returns suggestions with IDs
- `BatchUserResolutionError` - Batch resolution with detailed per-user errors

**MCP Tools**:
- `planner_searchUsers` - Search users by display name
- `planner_lookupUser` - Resolve single user identifier
- `planner_createTask` - Now supports `assignee` parameter (comma-separated)

**CLI Commands**:
- `user search-users` - Search users by name
- `user lookup-user` - Resolve user identifier
- `add --assignee` - Create task with assignees (comma-separated)
