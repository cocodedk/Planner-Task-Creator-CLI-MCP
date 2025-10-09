# Examples: Microsoft Planner Task Creator CLI

This document provides practical examples for common use cases.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Authentication](#authentication)
3. [Configuration](#configuration)
4. [Task Creation](#task-creation)
5. [Listing and Discovery](#listing-and-discovery)
6. [Advanced Scenarios](#advanced-scenarios)
7. [Shell Integration](#shell-integration)
8. [MCP Server Usage](#mcp-server-usage)

## Basic Usage

### First-Time Setup

```bash
# 1. Initialize authentication
python planner.py init-auth

# 2. Set your default plan and bucket
python planner.py set-defaults --plan "Work Projects" --bucket "To Do"

# 3. Create your first task
python planner.py add --title "My first task"
```

## Authentication

### Standard Authentication Flow

```bash
$ python planner.py init-auth

Authentication Required
Please visit: https://microsoft.com/devicelogin
Enter code: ABC123XYZ

# After completing authentication in browser:
✓ Authentication successful!
```

### Using Environment Variables

```bash
export TENANT_ID="12345678-1234-1234-1234-123456789abc"
export CLIENT_ID="87654321-4321-4321-4321-cba987654321"

python planner.py init-auth
```

### Using Config File Only

```bash
# Create config file
cat > ~/.planner-cli/config.json << 'EOF'
{
  "tenant_id": "12345678-1234-1234-1234-123456789abc",
  "client_id": "87654321-4321-4321-4321-cba987654321"
}
EOF

chmod 600 ~/.planner-cli/config.json

# Authenticate
python planner.py init-auth
```

## Configuration

### Setting Defaults

```bash
# Set both plan and bucket
python planner.py set-defaults \
  --plan "Q4 2024 Projects" \
  --bucket "In Progress"

# Output:
# ✓ Defaults saved: plan='Q4 2024 Projects', bucket='In Progress'
```

### Using Different Config Locations

```bash
# Use custom config path
export PLANNER_CONFIG_PATH="~/my-projects/.planner-config.json"

python planner.py set-defaults --plan "My Plan" --bucket "To Do"
```

### Priority Demonstration

```bash
# Config file has: plan="Plan A", bucket="Bucket A"
# Env vars have: PLANNER_DEFAULT_PLAN="Plan B"

# Using defaults (env var wins)
python planner.py add --title "Task 1"
# Uses: Plan B, Bucket A

# Using CLI flag (highest priority)
python planner.py add --title "Task 2" --plan "Plan C"
# Uses: Plan C, Bucket A
```

## Task Creation

### Simple Tasks

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

### Tasks with Labels

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

### Complete Task Examples

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

### Overriding Defaults

```bash
# Default plan is "Work", but use "Personal" for this task
python planner.py add \
  --title "Grocery shopping" \
  --plan "Personal" \
  --bucket "To Do"
```

## Listing and Discovery

### List All Plans

```bash
$ python planner.py list-plans

[
  {
    "id": "plan-id-1",
    "title": "Work Projects",
    "owner": "group-id-1",
    "groupName": "Engineering Team"
  },
  {
    "id": "plan-id-2",
    "title": "Personal Tasks",
    "owner": "group-id-2",
    "groupName": "My Personal Group"
  }
]
```

### List Buckets in a Plan

```bash
$ python planner.py list-buckets --plan "Work Projects"

[
  {
    "id": "bucket-id-1",
    "name": "To Do",
    "planId": "plan-id-1"
  },
  {
    "id": "bucket-id-2",
    "name": "In Progress",
    "planId": "plan-id-1"
  },
  {
    "id": "bucket-id-3",
    "name": "Done",
    "planId": "plan-id-1"
  }
]
```

### Using Plan IDs

```bash
# List buckets by plan ID
python planner.py list-buckets \
  --plan "12345678-1234-1234-1234-123456789abc"
```

## Advanced Scenarios

### Scripting and Automation

```bash
#!/bin/bash
# create-weekly-tasks.sh

# Set up environment
export TENANT_ID="..."
export CLIENT_ID="..."

# Authenticate once
python planner.py init-auth

# Create multiple tasks
tasks=(
  "Review pull requests"
  "Update documentation"
  "Team sync meeting"
  "Code review session"
  "Deploy to staging"
)

for task in "${tasks[@]}"; do
  python planner.py add \
    --title "$task" \
    --plan "Work Projects" \
    --bucket "This Week" \
    --due "2024-12-20"

  echo "Created: $task"
done
```

### Parsing Output

```bash
# Create task and extract task ID
output=$(python planner.py add --title "Test task" 2>/dev/null)
task_id=$(echo "$output" | jq -r '.taskId')
echo "Created task: $task_id"

# Check if task creation succeeded
if [ $? -eq 0 ]; then
  echo "Success!"
else
  echo "Failed!"
fi
```

### Error Handling

```bash
#!/bin/bash
# create-task-with-retry.sh

create_task() {
  python planner.py add --title "$1" 2>&1
}

output=$(create_task "Important task")
exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo "Task created successfully"
  echo "$output" | jq '.'
else
  echo "Error occurred:"
  echo "$output" | jq '.message'

  # Check error code
  error_code=$(echo "$output" | jq -r '.code')

  if [ "$error_code" == "NotFound" ]; then
    echo "Available options:"
    echo "$output" | jq '.candidates'
  fi
fi
```

### Batch Task Creation from CSV

```bash
#!/bin/bash
# import-tasks.csv:
# title,description,due_date,labels
# Task 1,Description 1,2024-12-25,Label1
# Task 2,Description 2,2024-12-26,Label2

while IFS=, read -r title desc due labels; do
  [ "$title" = "title" ] && continue  # Skip header

  python planner.py add \
    --title "$title" \
    --desc "$desc" \
    --due "$due" \
    --labels "$labels"

  sleep 1  # Rate limiting
done < import-tasks.csv
```

## Shell Integration

### Bash Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc

alias planner='python ~/.planner-cli/planner.py'
alias ptask='python ~/.planner-cli/planner.py add --title'
alias plist='python ~/.planner-cli/planner.py list-plans'
alias pbuckets='python ~/.planner-cli/planner.py list-buckets'

# Usage:
# ptask "Quick task"
# plist
# pbuckets --plan "Work"
```

### Fish Shell Functions

```fish
# Add to ~/.config/fish/functions/

# Function: planner.fish
function planner
    python ~/.planner-cli/planner.py $argv
end

# Function: ptask.fish
function ptask
    python ~/.planner-cli/planner.py add --title $argv
end

# Usage:
# ptask "Quick task"
# planner list-plans
```

### ZSH Completion (Basic)

```zsh
# Add to ~/.zshrc

_planner() {
  local commands
  commands=(
    'init-auth:Initialize authentication'
    'set-defaults:Set default plan and bucket'
    'list-plans:List all plans'
    'list-buckets:List buckets in a plan'
    'add:Create a new task'
  )

  _describe 'command' commands
}

compdef _planner planner
```

## MCP Server Usage

### In Claude Desktop

**Example 1: Simple Task Creation**
```
User: Can you create a task in my Planner called "Review Q4 metrics"?

Claude: I'll create that task for you.
[Uses planner_createTask tool]

Task created successfully:
- Task ID: abc123...
- Title: Review Q4 metrics
- URL: https://planner.cloud.microsoft/...
```

**Example 2: Task with Details**
```
User: Create a task titled "Prepare presentation" with a description
"Slides for quarterly review" and due date December 31st, 2024.

Claude: I'll create that task with all the details.
[Uses planner_createTask with desc and due parameters]

Task created:
- Title: Prepare presentation
- Description: Slides for quarterly review
- Due: 2024-12-31
```

**Example 3: List Plans First**
```
User: What plans do I have available?

Claude: Let me check your available plans.
[Uses planner_listPlans tool]

You have 3 plans:
1. Work Projects (Engineering Team)
2. Personal Tasks (My Personal Group)
3. Q4 2024 (Management)
```

**Example 4: Set Defaults**
```
User: Set my default plan to "Work Projects" and bucket to "This Week"

Claude: I'll update your defaults.
[Uses planner_setDefaults tool]

Defaults updated successfully.
```

### Using MCP Server Directly

If you're building your own MCP client:

```typescript
// Example MCP client code
const result = await client.callTool("planner_createTask", {
  title: "Implement new feature",
  plan: "Web Development",
  bucket: "Sprint 12",
  desc: "Add user profile customization",
  due: "2024-12-31",
  labels: "Label1,Label2"
});

console.log(result);
```

## Tips and Tricks

### Quick Daily Standup Tasks

```bash
#!/bin/bash
# daily-standup.sh

PLAN="Work Projects"
BUCKET="Today"
DATE=$(date -d "+1 day" +%Y-%m-%d)

python planner.py add --title "Daily standup" --plan "$PLAN" --bucket "$BUCKET" --due "$DATE"
python planner.py add --title "Code review" --plan "$PLAN" --bucket "$BUCKET" --due "$DATE"
python planner.py add --title "Update documentation" --plan "$PLAN" --bucket "$BUCKET" --due "$DATE"
```

### Template Tasks

```bash
# Create a function for common task types
create_bug_task() {
  python planner.py add \
    --title "BUG: $1" \
    --desc "$2" \
    --labels "Label1" \
    --plan "Bug Tracking" \
    --bucket "New Bugs"
}

create_feature_task() {
  python planner.py add \
    --title "FEATURE: $1" \
    --desc "$2" \
    --labels "Label2" \
    --plan "Development" \
    --bucket "Backlog"
}

# Usage:
create_bug_task "Login fails on mobile" "Users report unable to login on iOS"
create_feature_task "Dark mode" "Add dark mode theme option"
```

### Debugging

```bash
# Enable Python debugging
PYTHONPATH=. python -m pdb planner.py add --title "Debug task"

# Verbose HTTP requests (for development)
export PYTHONVERBOSE=1
python planner.py add --title "Test"

# Check what's in your config
cat ~/.planner-cli/config.json | jq '.'

# Verify authentication cache exists
ls -la ~/.planner-cli/msal_cache.bin
```

## Real-World Workflows

### Project Management Workflow

```bash
# 1. Start new project
python planner.py set-defaults --plan "New Project" --bucket "Planning"

# 2. Create initial tasks
python planner.py add --title "Project kickoff meeting" --due "2024-12-15"
python planner.py add --title "Requirements gathering" --due "2024-12-18"
python planner.py add --title "Technical design" --due "2024-12-20"

# 3. Move to implementation
python planner.py set-defaults --plan "New Project" --bucket "Development"

# 4. Create development tasks
python planner.py add --title "Setup repository" --labels "Label1"
python planner.py add --title "Implement core features" --labels "Label1,Label2"
```

### Personal Task Management

```bash
# Morning routine
python planner.py add \
  --title "Check emails" \
  --plan "Personal" \
  --bucket "Morning Routine" \
  --due $(date +%Y-%m-%d)

# Weekly review
python planner.py list-buckets --plan "Personal" | \
  jq -r '.[].name' | \
  while read bucket; do
    echo "Bucket: $bucket"
  done
```

This examples guide should help you get started with the Planner CLI for various scenarios!
