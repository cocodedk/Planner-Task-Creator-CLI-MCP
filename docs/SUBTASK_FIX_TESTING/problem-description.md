# Problem Description

## What Was Fixed

The 400 Bad Request error when adding or completing subtasks has been resolved. The issue was caused by including `@odata` metadata annotations in PATCH requests to the Microsoft Graph API.

## Root Cause

The Microsoft Graph API rejects PATCH requests containing `@odata` metadata annotations. These annotations are included in GET responses but must be stripped before sending PATCH requests.

## Impact

- **Subtask Creation**: Failed with 400 Bad Request
- **Subtask Completion**: Failed with 400 Bad Request
- **User Experience**: Users couldn't add or complete checklist items
- **API Compliance**: PATCH requests didn't follow Graph API requirements
