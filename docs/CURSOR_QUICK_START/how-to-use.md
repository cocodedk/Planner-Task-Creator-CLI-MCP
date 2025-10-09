# How to Use

## Step 1: Restart Cursor
**Important:** You must **completely quit** and restart Cursor (not just reload window)

## Step 2: Test the Integration

Open Cursor's AI chat (Cmd/Ctrl+L) and try these commands:

### Example 1: List Your Plans
```
Can you list my Microsoft Planner plans?
```

**Expected Response:**
Cursor AI will use the `planner_listPlans` tool and show you:
- ToDo II
- FITS
- Tasks

### Example 2: List Buckets
```
What buckets are in my FITS plan?
```

**Expected Response:**
Cursor AI will use `planner_listBuckets` and show:
- Done
- Review
- Doing
- To do

### Example 3: Create a Task
```
Create a task called "Review PR #123" in my FITS plan,
in the To do bucket, with description "Check the authentication changes"
and due date December 31, 2025
```

**Expected Response:**
Cursor AI will:
1. Use `planner_createTask` tool
2. Show task ID and confirmation
3. The task will appear in your Microsoft Planner!
