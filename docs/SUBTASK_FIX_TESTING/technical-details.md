# Technical Details

## Root Cause

The Microsoft Graph API rejects PATCH requests containing `@odata` metadata annotations. These annotations are included in GET responses but must be stripped before sending PATCH requests.

## Solution

Created a "clean_checklist" function that:
1. Copies existing checklist items
2. Strips @odata annotations
3. Keeps only required fields: title, isChecked, orderHint
4. Adds new items to the clean checklist
5. Sends clean payload to API

## Code Location

- `planner_lib/task_subtask_add.py` - Lines 32-65
- `planner_lib/task_subtask_complete.py` - Lines 47-111

## Before vs After

### Before (Failed)
```json
{
  "@odata.etag": "W/\"JzEtQ2hlY2tsaXN0SXRlbSA4QCcBAQEBAQEBAQEBAQEBAYCc=\"",
  "title": "New subtask",
  "isChecked": false,
  "orderHint": "8585234698740091215P]"
}
```

### After (Works)
```json
{
  "title": "New subtask",
  "isChecked": false,
  "orderHint": "8585234698740091215P]"
}
```

## Expected Behavior

### ✅ Success
- Subtasks should be added without 400 errors
- Subtasks should appear in Microsoft Planner web interface
- Checklist items should be properly ordered
- Completing subtasks should work correctly

### ❌ Previous Error (Now Fixed)
```
400 Bad Request: Invalid request payload
```
