# Subtask 400 Error Fix - Testing Guide

## ✅ Fix Status: COMPLETE

Branch: `fix/subtask-400-error`
Pull Request: https://github.com/cocodedk/Planner-Task-Creator-CLI-MCP/pull/new/fix/subtask-400-error

## What Was Fixed

The 400 Bad Request error when adding or completing subtasks has been resolved. The issue was caused by including `@odata` metadata annotations in PATCH requests to the Microsoft Graph API.

### Changes Made

1. **planner_lib/task_subtask_add.py**
   - Clean checklist data before PATCH requests
   - Remove @odata annotations from request payload
   - Improved orderHint generation
   - Better 400 error messages for debugging

2. **planner_lib/task_subtask_complete.py**
   - Clean checklist data before PATCH requests
   - Remove @odata annotations from request payload
   - Enhanced error handling

### Test Results

✅ All 68 tests pass
✅ 9 subtask-specific tests verified
✅ TypeScript builds successfully
✅ No linter errors

## Testing the Fix

### Option 1: Using MCP Tools (Recommended)

**Important:** The MCP tool is called `planner_addSubtask` (not a different name - it adds checklist items which are called "subtasks" in the UI).

**Note:** If the tool doesn't appear, reload the MCP connection in Cursor (the server has been rebuilt with the fix).

1. **Create a test task:**
```typescript
planner_createTask({
  title: "Test Subtask Fix",
  plan: "FITS",
  bucket: "To do",
  desc: "Testing subtask functionality after fix"
})
```

2. **Add first subtask:**
```typescript
planner_addSubtask({
  task: "<task-id-from-step-1>",
  subtask: "First subtask - Verify API works",
  plan: "FITS"
})
```

3. **Add second subtask:**
```typescript
planner_addSubtask({
  task: "<task-id-from-step-1>",
  subtask: "Second subtask - Confirm no 400 error",
  plan: "FITS"
})
```

4. **List subtasks:**
```typescript
planner_listSubtasks({
  task: "<task-id-from-step-1>",
  plan: "FITS"
})
```

5. **Complete a subtask:**
```typescript
planner_completeSubtask({
  task: "<task-id-from-step-1>",
  subtask: "First subtask - Verify API works",
  plan: "FITS"
})
```

### Option 2: Using CLI

**Requirements:** Valid TENANT_ID and CLIENT_ID in config or environment

```bash
# Activate virtual environment
source venv/bin/activate

# Create task
python3 planner.py add --plan FITS --bucket "To do" \
  --title "Test Subtask Fix" \
  --desc "Testing subtask functionality"

# Add subtasks (use task ID from previous command)
python3 planner.py add-subtask-cmd \
  --task <task-id> \
  --subtask "First subtask - Verify API works" \
  --plan FITS

python3 planner.py add-subtask-cmd \
  --task <task-id> \
  --subtask "Second subtask - Confirm no 400 error" \
  --plan FITS

# List subtasks
python3 planner.py list-subtasks-cmd \
  --task <task-id> \
  --plan FITS

# Complete a subtask
python3 planner.py complete-subtask-cmd \
  --task <task-id> \
  --subtask "First subtask - Verify API works" \
  --plan FITS
```

## ✅ Test Task Created and Verified

A test task has been created with 2 subtasks:
- **Task ID:** `lDTneZMnIE2mUStuz_hxjZgAPqYz`
- **Plan:** FITS
- **Bucket:** To do
- **Title:** "Test Subtask Fix - Verify 400 Error Resolution"

**Subtasks Added Successfully:**
1. ✅ "First subtask - Verify API works" (ID: `df0ad5b4-1604-4dd9-9c4c-211001d3dcb9`)
2. ✅ "Second subtask - Confirm no 400 error" (ID: `45c979f1-0f75-49c0-a3b8-92fa23cba26e`)

Both subtasks are visible in Microsoft Planner and working correctly!

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

## Next Steps

1. **Test the fix** using either method above
2. **Review the PR** at the provided link
3. **Merge to main** once testing confirms the fix works
4. **Update documentation** if needed

## Technical Details

### Root Cause
The Microsoft Graph API rejects PATCH requests containing `@odata` metadata annotations. These annotations are included in GET responses but must be stripped before sending PATCH requests.

### Solution
Created a "clean_checklist" function that:
1. Copies existing checklist items
2. Strips @odata annotations
3. Keeps only required fields: title, isChecked, orderHint
4. Adds new items to the clean checklist
5. Sends clean payload to API

### Code Location
- `planner_lib/task_subtask_add.py` - Lines 32-65
- `planner_lib/task_subtask_complete.py` - Lines 47-111
