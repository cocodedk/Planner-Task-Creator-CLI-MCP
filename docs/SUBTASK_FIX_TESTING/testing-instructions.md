# Testing Instructions

## Option 1: Using MCP Tools (Recommended)

**Important:** The MCP tool is called `planner_addSubtask` (not a different name - it adds checklist items which are called "subtasks" in the UI).

**Note:** If the tool doesn't appear, reload the MCP connection in Cursor (the server has been rebuilt with the fix).

### Step 1: Create a test task
```typescript
planner_createTask({
  title: "Test Subtask Fix",
  plan: "FITS",
  bucket: "To do",
  desc: "Testing subtask functionality after fix"
})
```

### Step 2: Add first subtask
```typescript
planner_addSubtask({
  task: "<task-id-from-step-1>",
  subtask: "First subtask - Verify API works",
  plan: "FITS"
})
```

### Step 3: Add second subtask
```typescript
planner_addSubtask({
  task: "<task-id-from-step-1>",
  subtask: "Second subtask - Confirm no 400 error",
  plan: "FITS"
})
```

### Step 4: List subtasks
```typescript
planner_listSubtasks({
  task: "<task-id-from-step-1>",
  plan: "FITS"
})
```

### Step 5: Complete a subtask
```typescript
planner_completeSubtask({
  task: "<task-id-from-step-1>",
  subtask: "First subtask - Verify API works",
  plan: "FITS"
})
```

## Option 2: Using CLI

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
