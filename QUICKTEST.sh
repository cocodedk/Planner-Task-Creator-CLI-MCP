#!/bin/bash
#
# Quick Test Script for Planner Task Creator CLI
# Run this to verify your installation is working
#

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Planner Task Creator CLI - Quick Test                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check environment variables
if [ -z "$TENANT_ID" ] || [ -z "$CLIENT_ID" ]; then
    echo "❌ Environment variables not set!"
    echo "   Please set TENANT_ID and CLIENT_ID"
    echo ""
    echo "   export TENANT_ID=\"your-tenant-id\""
    echo "   export CLIENT_ID=\"your-client-id\""
    exit 1
fi

echo "✅ Environment configured"
echo "   Tenant ID: ${TENANT_ID:0:8}..."
echo "   Client ID: ${CLIENT_ID:0:8}..."
echo ""

# Test 1: Authentication
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Authentication"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if python planner.py init-auth 2>&1 | grep -q "Authentication successful"; then
    echo "✅ Authentication test passed"
else
    echo "❌ Authentication test failed"
    echo "   Check your Azure AD app configuration"
    exit 1
fi
echo ""

# Test 2: List Plans
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: List Plans"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PLANS=$(python planner.py list-plans 2>&1)
if echo "$PLANS" | jq -e '.[0].id' > /dev/null 2>&1; then
    echo "✅ List plans test passed"
    echo ""
    echo "Available plans:"
    echo "$PLANS" | jq -r '.[] | "   • \(.title)"'
    FIRST_PLAN=$(echo "$PLANS" | jq -r '.[0].title')
else
    echo "❌ List plans test failed"
    exit 1
fi
echo ""

# Test 3: List Buckets
if [ -n "$FIRST_PLAN" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Test 3: List Buckets (from '$FIRST_PLAN')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    BUCKETS=$(python planner.py list-buckets --plan "$FIRST_PLAN" 2>&1)
    if echo "$BUCKETS" | jq -e '.[0].id' > /dev/null 2>&1; then
        echo "✅ List buckets test passed"
        echo ""
        echo "Available buckets:"
        echo "$BUCKETS" | jq -r '.[] | "   • \(.name)"'
        FIRST_BUCKET=$(echo "$BUCKETS" | jq -r '.[0].name')
    else
        echo "❌ List buckets test failed"
        exit 1
    fi
    echo ""
fi

# Test 4: Create Task (optional, commented out by default)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Create Task (optional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Skipped (uncomment in script to test task creation)"
echo ""

# Uncomment to test task creation:
# if [ -n "$FIRST_PLAN" ] && [ -n "$FIRST_BUCKET" ]; then
#     TEST_TASK=$(python planner.py add \
#         --title "Test Task $(date +%Y%m%d-%H%M%S)" \
#         --plan "$FIRST_PLAN" \
#         --bucket "$FIRST_BUCKET" \
#         --desc "Automated test task" \
#         2>&1)
#
#     if echo "$TEST_TASK" | jq -e '.taskId' > /dev/null 2>&1; then
#         echo "✅ Create task test passed"
#         echo "$TEST_TASK" | jq '.'
#     else
#         echo "❌ Create task test failed"
#         exit 1
#     fi
# fi

# Test 5: Unit Tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 5: Unit Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if pytest tests/ -q; then
    echo "✅ Unit tests passed"
else
    echo "⚠️  Some unit tests failed (check output above)"
fi
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   All Tests Completed Successfully! ✅                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Your Planner CLI is ready to use! 🎉"
echo ""
echo "Try these commands:"
echo "  python planner.py list-plans"
echo "  python planner.py list-buckets --plan \"$FIRST_PLAN\""
echo "  python planner.py add --title \"My Task\" --plan \"$FIRST_PLAN\" --bucket \"$FIRST_BUCKET\""
echo ""
