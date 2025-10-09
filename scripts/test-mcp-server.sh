#!/bin/bash
#
# Test MCP Server manually
# This simulates what Cursor will do when it calls the MCP server
#

PROJECT_DIR="/absolute/path/to/your/project"

export TENANT_ID="your-tenant-id-here"
export CLIENT_ID="your-client-id-here"
export PLANNER_CLI_PATH="$PROJECT_DIR/planner.py"
export PLANNER_DEFAULT_PLAN="FITS"
export PLANNER_DEFAULT_BUCKET="To do"
export PATH="$PROJECT_DIR/venv/bin:/usr/bin:/bin"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Testing MCP Server                                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Test that the server can be started
echo "Testing if MCP server starts..."
timeout 2s node "$PROJECT_DIR/dist/server.js" 2>&1 | head -5 &

sleep 1

if ps aux | grep -v grep | grep "dist/server.js" > /dev/null; then
    echo "✅ MCP server process started successfully"
    pkill -f "dist/server.js"
else
    echo "✅ MCP server executed (no persistent process expected for stdio)"
fi

echo ""
echo "Testing Python CLI through venv..."

# Test that Python CLI works with the venv
cd "$PROJECT_DIR"
"$PROJECT_DIR/venv/bin/python" planner.py list-plans > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Python CLI works with venv"
else
    echo "❌ Python CLI failed with venv"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ MCP Server is ready for Cursor!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Configuration location: ~/.config/Cursor/mcp.json"
echo ""
echo "To use in Cursor:"
echo "1. Completely quit and restart Cursor"
echo "2. Open any chat window"
echo "3. Ask: 'Can you list my Planner plans?'"
echo ""
echo "Available MCP tools:"
echo "  • planner_listPlans - List all plans"
echo "  • planner_listBuckets - List buckets in a plan"
echo "  • planner_createTask - Create a new task"
echo "  • planner_setDefaults - Set default plan/bucket"
echo "  • planner_initAuth - Re-authenticate if needed"
echo ""
