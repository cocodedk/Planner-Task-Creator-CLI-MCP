# Quick Setup Script

The `scripts/setup-cursor-mcp.sh` script:

```bash
#!/bin/bash

PROJECT_DIR="/absolute/path/to/your/project"
CONFIG_DIR="$HOME/.config/Cursor"
CONFIG_FILE="$CONFIG_DIR/mcp.json"

echo "Setting up Planner MCP for Cursor..."

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Create the configuration
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "planner": {
      "command": "node",
      "args": [
        "$PROJECT_DIR/dist/server.js"
      ],
      "env": {
        "TENANT_ID": "your-tenant-id-here",
        "CLIENT_ID": "your-client-id-here",
        "PLANNER_CLI_PATH": "$PROJECT_DIR/planner.py",
        "PLANNER_DEFAULT_PLAN": "FITS",
        "PLANNER_DEFAULT_BUCKET": "To do",
        "PYTHON_PATH": "$PROJECT_DIR/venv/bin/python"
      }
    }
  }
}
EOF

echo "✅ Configuration created at: $CONFIG_FILE"
echo ""
echo "Next steps:"
echo "1. Update PROJECT_DIR in this script with your actual path"
echo "2. Update TENANT_ID and CLIENT_ID with your Azure credentials"
echo "3. Restart Cursor completely"
echo "4. Test by asking: 'Can you list my Planner plans?'"
echo ""
echo "Configuration contents:"
cat "$CONFIG_FILE"
```

Run it:
```bash
chmod +x scripts/setup-cursor-mcp.sh
./scripts/setup-cursor-mcp.sh
```
