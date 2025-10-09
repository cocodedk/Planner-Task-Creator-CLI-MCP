# User Search Feature - Implementation Summary

## Overview

Enhanced the task assignment feature with user search functionality, allowing partial name matching for better user experience.

## Problem Statement

Initial implementation required exact email addresses or User IDs for task assignment. This was cumbersome when users only knew teammates' first names (e.g., "Iman" instead of "iman.karimi@company.com").

## Solution

Implemented a three-tier resolution strategy:

1. **GUID Direct Return**: If input is a valid GUID, return immediately
2. **Exact Match**: Try direct API lookup (email/UPN)
3. **Partial Name Search**: Fall back to display name search with `startswith` filter

## Technical Implementation

### 1. Enhanced User Resolution (`planner_lib/resolution_users.py`)

#### New Function: `search_users_by_name`
```python
def search_users_by_name(token: str, search_term: str) -> List[Dict[str, Any]]:
    """
    Search for users whose display name starts with the search term.

    Uses Graph API $filter query:
    GET /users?$filter=startswith(displayName,'{term}')&$select=id,displayName,userPrincipalName,mail
    """
```

#### Enhanced Function: `resolve_user`
```python
def resolve_user(token: str, user_identifier: str, enable_search: bool = True) -> str:
    """
    Resolve with fallback strategy:
    1. Check if GUID → return directly
    2. Try exact match (email/UPN)
    3. If enabled, try partial name search:
       - Single match → use it
       - Multiple matches → raise AmbiguousUser error with suggestions
    """
```

### 2. CLI Commands (`planner_lib/cli_user_commands.py`)

#### Command: `user search <query>`
Search for users by display name:
```bash
$ planner.py user search "Iman" --verbose

Found 1 user(s) matching 'Iman':

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Display Name ┃ Email                    ┃ User ID                            ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Iman Karimi  │ iman.karimi@company.com  │ a1b2c3d4-e5f6-7890-abcd-ef1234567890│
└─────────────┴──────────────────────────┴────────────────────────────────────┘

Tip: Use the email or User ID with --assignee flag
```

#### Command: `user lookup <identifier>`
Resolve user identifier to full details:
```bash
$ planner.py user lookup "Iman" --verbose

✓ User found:
  Name: Iman Karimi
  Email: iman.karimi@company.com
  User ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Title: Software Engineer
  Department: Engineering
```

### 3. MCP Server Integration

Added two new MCP tools:

#### Tool: `planner_searchUsers`
```typescript
{
  name: "planner_searchUsers",
  description: "Search for users in Azure AD by display name. Supports partial name matching.",
  inputSchema: {
    properties: {
      query: {
        type: "string",
        description: "Search term (name or partial name, e.g., 'John', 'Iman')"
      }
    },
    required: ["query"]
  }
}
```

#### Tool: `planner_lookupUser`
```typescript
{
  name: "planner_lookupUser",
  description: "Resolve a user identifier to full user details.",
  inputSchema: {
    properties: {
      user: {
        type: "string",
        description: "User email, UPN, User ID, or partial name"
      },
      noSearch: {
        type: "boolean",
        description: "Disable partial name search fallback"
      }
    },
    required: ["user"]
  }
}
```

## Usage Examples

### Scenario 1: Single Match (Auto-resolved)
```bash
# User only knows first name
$ planner.py add --title "Code Review" --assignee "Iman"

# Behind the scenes:
# 1. Not a GUID ❌
# 2. Exact match fails (no user with email "Iman") ❌
# 3. Search: startswith(displayName,'Iman')
# 4. Found 1 result: "Iman Karimi" ✅
# 5. Use user ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890

✓ Task created and assigned to Iman Karimi
```

### Scenario 2: Multiple Matches (Error with Suggestions)
```bash
$ planner.py add --title "Meeting" --assignee "John"

# Error output:
{
  "code": "AmbiguousUser",
  "message": "Multiple users found matching 'John'. Please be more specific.",
  "suggestions": [
    "John Smith (john.smith@company.com)",
    "John Doe (john.doe@company.com)",
    "Johnny Walker (johnny.walker@company.com)"
  ],
  "hint": "Use full email address or User ID for exact match"
}
```

### Scenario 3: Interactive Search Workflow
```bash
# Step 1: Search for users
$ planner.py user search "John"

{
  "count": 3,
  "users": [
    {
      "id": "user-id-1",
      "displayName": "John Smith",
      "email": "john.smith@company.com"
    },
    {
      "id": "user-id-2",
      "displayName": "John Doe",
      "email": "john.doe@company.com"
    }
  ]
}

# Step 2: Use specific email
$ planner.py add --title "Meeting" --assignee "john.smith@company.com"
✓ Task created
```

### Scenario 4: MCP Usage (AI Assistant)
```
User: "Assign this task to Iman"

AI Assistant:
1. Calls planner_lookupUser(user: "Iman")
2. Receives: { "id": "a1b2c3d4...", "displayName": "Iman Karimi", "email": "iman.karimi@company.com" }
3. Calls planner_createTask(title: "...", assignee: "iman.karimi@company.com")
4. Responds: "✓ Task created and assigned to Iman Karimi"
```

## Error Handling

### Error 1: User Not Found
```json
{
  "code": "UserNotFound",
  "message": "No users found matching 'NonExistentUser'"
}
```

### Error 2: Ambiguous User (Multiple Matches)
```json
{
  "code": "AmbiguousUser",
  "message": "Multiple users found matching 'John'. Please be more specific.",
  "suggestions": [
    "John Smith (john.smith@company.com)",
    "John Doe (john.doe@company.com)"
  ],
  "hint": "Use full email address or User ID for exact match"
}
```

### Error 3: Disable Search (Exact Match Only)
```bash
# Force exact match only (no search fallback)
$ planner.py user lookup "Iman" --no-search

{
  "code": "UserNotFound",
  "message": "User 'Iman' not found or not accessible"
}
```

## API Requirements

### Graph API Endpoint Used
```
GET https://graph.microsoft.com/v1.0/users?$filter=startswith(displayName,'{searchTerm}')&$select=id,displayName,userPrincipalName,mail
```

### Required Permissions
- `User.Read.All` (recommended) - Read all users' full profiles
- OR `User.ReadBasic.All` - Read all users' basic profiles

These permissions should already be granted during the initial authentication setup.

## Testing

### Unit Tests (`tests/test_user_search.py`)

Comprehensive test coverage for:
- ✅ Single search result
- ✅ Multiple search results
- ✅ No search results
- ✅ API error handling
- ✅ GUID direct return
- ✅ Exact email match
- ✅ Single search match (auto-resolve)
- ✅ Ambiguous search (multiple matches)
- ✅ User not found (search disabled)
- ✅ User not found (search enabled)
- ✅ Batch resolution
- ✅ Whitespace handling
- ✅ Error propagation

Run tests:
```bash
pytest tests/test_user_search.py -v
```

### Integration Testing

1. **Test with single match:**
   ```bash
   planner.py add --title "Test" --assignee "<partial-name-with-single-match>"
   ```

2. **Test with multiple matches:**
   ```bash
   planner.py add --title "Test" --assignee "John"
   # Should show suggestions
   ```

3. **Test search command:**
   ```bash
   planner.py user search "Test"
   ```

4. **Test lookup command:**
   ```bash
   planner.py user lookup "<email-or-name>"
   ```

## Benefits

### User Experience
- ✅ Natural language: Users can type partial names
- ✅ Faster workflow: No need to look up full email addresses
- ✅ Clear errors: Ambiguous matches provide helpful suggestions
- ✅ Discovery: Search command helps find correct identifiers

### Technical
- ✅ Backward compatible: Exact matches still work
- ✅ Flexible: Search can be disabled with `enable_search=False`
- ✅ Efficient: GUIDs bypass all API calls
- ✅ Robust: Handles errors gracefully

## Limitations

1. **Partial Match Only Checks Display Name Start**
   - `startswith(displayName,'John')` will match "John Smith" but not "Mary John"
   - Could be enhanced with full-text search using `$search` (requires different Graph API header)

2. **No Interactive Selection in MCP**
   - CLI could be enhanced to prompt user to select from multiple matches
   - MCP server (non-interactive) always returns error with suggestions

3. **Performance**
   - Each partial name adds 1-2 additional API calls
   - Consider caching for high-volume scenarios

## Future Enhancements

1. **Fuzzy Search**: Use `$search` parameter instead of `$filter` for more flexible matching
2. **Email Search**: Also search by email field, not just display name
3. **Recent Users Cache**: Cache recently resolved users for faster lookups
4. **Interactive Selection**: In CLI mode, allow user to pick from multiple matches
5. **Alias Support**: Support custom aliases (e.g., "iman" → "iman.karimi@company.com")

## Files Modified

1. **`planner_lib/resolution_users.py`** - Enhanced with search functionality
2. **`planner_lib/cli_user_commands.py`** - New CLI commands (search, lookup)
3. **`planner_lib/cli_commands.py`** - Register user commands
4. **`src/server/tools.ts`** - Add MCP tool definitions
5. **`src/server/handlers-users.ts`** - New MCP handlers
6. **`src/server/handlers.ts`** - Route to user handlers
7. **`tests/test_user_search.py`** - Comprehensive unit tests

## Documentation

- **This file**: Implementation and usage summary
- **`005-implementation-summary.md`**: Updated with partial name support note
- **CLI help**: `planner.py user --help`
