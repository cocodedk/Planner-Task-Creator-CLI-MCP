# Advanced Scenarios

## Scripting and Automation

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

## Parsing Output

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

## Error Handling

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

## Batch Task Creation from CSV

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
