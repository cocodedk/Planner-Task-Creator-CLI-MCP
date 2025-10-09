# Azure AD Configuration Used

## Configuration Details

- **Tenant ID:** `your-tenant-id-here` (obfuscated for security)
- **Client ID:** `your-client-id-here` (obfuscated for security)
- **Application Name:** Planner Task Creator CLI

## Setup Changes Made

### 1. Fixed Scope Configuration
**Issue:** `offline_access` scope caused authentication errors when explicitly included.

**Solution:** Removed `offline_access` from `REQUIRED_SCOPES` as MSAL includes it automatically.

```python
# Before
REQUIRED_SCOPES = ["Tasks.ReadWrite", "Group.ReadWrite.All", "offline_access"]

# After
REQUIRED_SCOPES = ["Tasks.ReadWrite"]  # Simplified for testing
```

### 2. Fixed Python 3.13 Compatibility
**Issue:** Typer 0.12.5 had compatibility issues with Python 3.13.

**Solution:** Upgraded to typer 0.19.2 and downgraded rich to <13.0.0 for stability.

```txt
# Updated requirements.txt
typer==0.19.2
rich>=10.11.0,<13.0.0
```

### 3. Updated Documentation
Updated both `SETUP_GUIDE.md` and `SETUP_WITHOUT_AZURE_SUBSCRIPTION.md` to:
- Remove `offline_access` from the required permissions list
- Add note that `Group.ReadWrite.All` requires admin consent
- Clarify that `offline_access` is automatically included by MSAL
