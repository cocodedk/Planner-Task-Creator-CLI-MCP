# Configuration

## Setting Defaults

```bash
# Set both plan and bucket
python planner.py set-defaults \
  --plan "Q4 2024 Projects" \
  --bucket "In Progress"

# Output:
# ✓ Defaults saved: plan='Q4 2024 Projects', bucket='In Progress'
```

## Using Different Config Locations

```bash
# Use custom config path
export PLANNER_CONFIG_PATH="~/my-projects/.planner-config.json"

python planner.py set-defaults --plan "My Plan" --bucket "To Do"
```

## Priority Demonstration

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
