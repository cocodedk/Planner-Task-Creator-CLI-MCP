# Issues Found and Fixed

## Issue 1: offline_access Scope Error

**Error Message:**
```
You cannot use any scope value that is reserved.
Your input: ['Group.ReadWrite.All', 'Tasks.ReadWrite', 'offline_access']
The reserved list: ['offline_access', 'profile', 'openid']
```

**Fix:** Removed `offline_access` from REQUIRED_SCOPES list.

## Issue 2: Public Client Flows Not Enabled

**Error Message:**
```
AADSTS7000218: The request body must contain the following parameter:
'client_assertion' or 'client_secret'.
```

**Fix:** User enabled "Allow public client flows" in Azure AD app settings.

## Issue 3: Typer/Python 3.13 Incompatibility

**Error Message:**
```
TypeError: Parameter.make_metavar() missing 1 required positional argument: 'ctx'
```

**Fix:** Upgraded typer from 0.12.5 to 0.19.2 and adjusted rich version.
