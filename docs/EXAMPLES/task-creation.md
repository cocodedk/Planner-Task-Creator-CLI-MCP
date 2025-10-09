# Task Creation

## Simple Tasks

```bash
# Minimal task (uses defaults)
python planner.py add --title "Review code"

# Task with description
python planner.py add \
  --title "Write documentation" \
  --desc "Complete API documentation for new endpoints"

# Task with due date
python planner.py add \
  --title "Submit report" \
  --due "2024-12-31"
```

## Tasks with Labels

```bash
# Single label
python planner.py add \
  --title "Bug fix" \
  --labels "Label1"

# Multiple labels
python planner.py add \
  --title "Feature development" \
  --labels "Label1,Label3,Label5"

# Case insensitive
python planner.py add \
  --title "Documentation" \
  --labels "label2,LABEL4"
```

## Complete Task Examples

```bash
# Full-featured task
python planner.py add \
  --title "Implement user authentication" \
  --plan "Web App Development" \
  --bucket "In Progress" \
  --desc "Add OAuth 2.0 authentication with social login support" \
  --due "2024-12-25" \
  --labels "Label1,Label2" \
  --verbose

# Output:
# {
#   "taskId": "abc123...",
#   "webUrl": "https://planner.cloud.microsoft/...",
#   "bucketId": "xyz789..."
# }
# ✓ Task created: Implement user authentication
#   Task ID: abc123...
#   URL: https://planner.cloud.microsoft/...
```

## Overriding Defaults

```bash
# Default plan is "Work", but use "Personal" for this task
python planner.py add \
  --title "Grocery shopping" \
  --plan "Personal" \
  --bucket "To Do"
```
