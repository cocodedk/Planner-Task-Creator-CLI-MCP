# Verification

## Test CLI Directly

```bash
# List plans
python planner.py list-plans

# List buckets
python planner.py list-buckets --plan "Your Plan"

# Create task
python planner.py add \
  --title "Test task" \
  --desc "Testing the CLI" \
  --due "2024-12-31" \
  --labels "Label1" \
  --verbose
```

## Test MCP Server (if installed)

In Claude Desktop, try asking:
```
"Can you create a task in my Planner called 'Test from Claude'?"
```

Claude should use the `planner_createTask` tool.
