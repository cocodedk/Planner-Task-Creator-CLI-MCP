# Usage Examples

## Python CLI
```bash
# Initialize
python planner.py init-auth
python planner.py set-defaults --plan "Work" --bucket "To Do"

# Create tasks
python planner.py add --title "Complete report"
python planner.py add \
  --title "Review code" \
  --desc "PR #123" \
  --due "2024-12-31" \
  --labels "Label1,Label2"

# List resources
python planner.py list-plans
python planner.py list-buckets --plan "Work"
```

## MCP Server
```json
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": ["/path/to/dist/server.js"],
      "env": {
        "TENANT_ID": "...",
        "CLIENT_ID": "..."
      }
    }
  }
}
```
