# Task Assignment Permission Requirements

## Issue: Task Assignment by Email Fails Without User.Read.All

**Symptom**: When attempting to assign tasks by email address (e.g., `bba@l7consulting.dk`), the assignment fails silently or returns `UserNotFound` error.

**Root Cause**: The app requires `User.Read.All` or `User.ReadBasic.All` permission to:
- Look up users by email address via Graph API `/users/{email}` endpoint
- Search users by display name via Graph API `/users?$filter=startswith(...)` endpoint

**Required Permissions**:
- `User.Read.All` (delegated, requires admin consent) - **REQUIRED for email/name-based assignment**
- `User.ReadBasic.All` (delegated, requires admin consent) - Alternative with limited profile access
- Without these permissions, the Graph API returns 401 Unauthorized for user lookup operations

**Solution**:
1. Go to Azure Portal → Azure AD → App Registrations → Your App
2. Click **API permissions**
3. Add **Microsoft Graph** → **Delegated permissions** → `User.Read.All`
4. Click **Grant admin consent for [Your Tenant]** (requires admin rights)
5. Re-authenticate: `python planner.py init-auth`
6. Test assignment: `python planner.py add --title "Test" --assignee "user@domain.com"`

**Workaround Without Permission**:
- Users can still be assigned using their Azure AD User ID (GUID) directly
- Example: `python planner.py add --title "Test" --assignee "12345678-1234-1234-1234-123456789abc"`

**Status**:
- ✅ Feature implemented and working when permissions are granted
- ⚠️ Requires admin consent for `User.Read.All` permission
