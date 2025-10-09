#!/bin/bash

PROJECT_DIR="/absolute/path/to/your/project"
CONFIG_DIR="$HOME/.config/Cursor"
CONFIG_FILE="$CONFIG_DIR/mcp.json"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Setting up Planner MCP for Cursor                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Check if mcp.json already exists
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Configuration file already exists at: $CONFIG_FILE"
    echo ""
    read -p "Do you want to backup and replace it? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d-%H%M%S)"
        echo "✅ Backup created"
    else
        echo "❌ Setup cancelled. You can manually merge the configuration."
        echo "   See CURSOR_SETUP.md for details."
        exit 1
    fi
fi

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
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  IMPORTANT: Before running this script, update:"
echo "   - PROJECT_DIR with your actual project path"
echo "   - TENANT_ID with your Azure AD tenant ID"
echo "   - CLIENT_ID with your Azure AD application client ID"
echo ""
echo "1. 🔄 Completely quit and restart Cursor"
echo ""
echo "2. 🧪 Test by asking Cursor AI:"
echo "   • 'Can you list my Microsoft Planner plans?'"
echo "   • 'What buckets are in my FITS plan?'"
echo "   • 'Create a task called Test in my FITS plan'"
echo ""
echo "3. 📋 View configuration:"
cat "$CONFIG_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Troubleshooting:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "If the server doesn't start, check:"
echo "  - Cursor MCP logs (usually in Cursor's debug console)"
echo "  - Test manually: node dist/server.js"
echo "  - Ensure Python venv is working: source venv/bin/activate"
echo ""
echo "For more help, see: CURSOR_SETUP.md"
echo ""
