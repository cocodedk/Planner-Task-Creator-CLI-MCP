# Cursor Quick Start Guide

## ✅ Setup Complete!

Your Planner MCP server is configured and ready to use in Cursor!

## 🚀 How to Use

### Step 1: Restart Cursor
**Important:** You must **completely quit** and restart Cursor (not just reload window)

### Step 2: Test the Integration

Open Cursor's AI chat (Cmd/Ctrl+L) and try these commands:

#### Example 1: List Your Plans
```
Can you list my Microsoft Planner plans?
```

**Expected Response:**
Cursor AI will use the `planner_listPlans` tool and show you:
- ToDo II
- FITS
- Tasks

#### Example 2: List Buckets
```
What buckets are in my FITS plan?
```

**Expected Response:**
Cursor AI will use `planner_listBuckets` and show:
- Done
- Review
- Doing
- To do

#### Example 3: Create a Task
```
Create a task called "Review PR #123" in my FITS plan,
in the To do bucket, with description "Check the authentication changes"
and due date December 31, 2025
```

**Expected Response:**
Cursor AI will:
1. Use `planner_createTask` tool
2. Show task ID and confirmation
3. The task will appear in your Microsoft Planner!

## 🎯 What You Can Do

### Natural Language Commands

You can ask Cursor AI to:

✅ **List things:**
- "Show me all my Planner plans"
- "What are the buckets in my Tasks plan?"

✅ **Create tasks:**
- "Add a task to my FITS plan"
- "Create a task called X in bucket Y"
- "Make a task with due date next Friday"

✅ **Set defaults:**
- "Set FITS as my default plan"
- "Make 'To do' my default bucket"

✅ **Re-authenticate:**
- "Initialize Planner authentication"

### More Examples

```
Create 3 tasks in my FITS plan:
1. "Update documentation" in To do
2. "Review code" in Doing
3. "Deploy changes" in Review
```

```
Add a high-priority task called "Fix bug #456"
to my Tasks plan with Label1
```

## 🔧 Configuration Details

Your MCP server is configured with:

- **Config File:** `~/.config/Cursor/mcp.json`
- **Default Plan:** FITS (or your chosen plan)
- **Default Bucket:** To do (or your chosen bucket)
- **CLI Path:** `/absolute/path/to/your/project/planner.py`
- **Server:** `/absolute/path/to/your/project/dist/server.js`

## 🐛 Troubleshooting

### MCP Server Not Working?

1. **Check Cursor's MCP status:**
   - Look for MCP server indicators in Cursor UI
   - Check Cursor's developer console (Help → Toggle Developer Tools)

2. **Test the CLI manually:**
   ```bash
   cd /absolute/path/to/your/project
   source venv/bin/activate
   python planner.py list-plans
   ```

3. **Test the MCP server:**
   ```bash
   cd /absolute/path/to/your/project
   ./scripts/test-mcp-server.sh
   ```

4. **Verify configuration:**
   ```bash
   cat ~/.config/Cursor/mcp.json
   ```

### Common Issues

**Issue:** "Server failed to start"
- **Fix:** Ensure Cursor was fully restarted (quit, don't just reload)
- **Fix:** Check that Node.js is installed: `node --version`
- **Fix:** Verify paths are absolute in `mcp.json`

**Issue:** "Authentication failed"
- **Fix:** Run `python planner.py init-auth` manually first
- **Fix:** Check token cache exists: `ls ~/.planner-cli/msal_cache.bin`

**Issue:** "Cannot find module"
- **Fix:** Rebuild the server: `npm run build`

**Issue:** "Python dependencies missing"
- **Fix:** Reinstall: `source venv/bin/activate && pip install -r requirements.txt`

## 📊 Available MCP Tools

| Tool Name | Description | Required Args |
|-----------|-------------|---------------|
| `planner_listPlans` | List all accessible plans | None |
| `planner_listBuckets` | List buckets in a plan | `plan` |
| `planner_createTask` | Create a new task | `title` |
| `planner_setDefaults` | Set default plan/bucket | `plan`, `bucket` |
| `planner_initAuth` | Re-authenticate | None |

## 🎓 Tips & Best Practices

### 1. Set Your Defaults
Makes creating tasks easier:
```
Set FITS as my default plan and "To do" as my default bucket
```

Now you can create tasks without specifying plan/bucket each time:
```
Create a task called "Quick task"
```

### 2. Use Descriptive Task Names
```
✅ Good: "Review authentication PR #123"
❌ Bad: "Review"
```

### 3. Add Due Dates
```
Create a task due next Friday
Create a task due 2025-12-31
```

### 4. Use Labels for Priority/Categories
```
Create a task with Label1 (high priority)
Add a task with Label3 (bug category)
```

## 🔄 Updating the Configuration

If you need to change settings:

1. Edit the config file:
   ```bash
   nano ~/.config/Cursor/mcp.json
   ```

2. Change default plan/bucket or other settings

3. Restart Cursor completely

Or run the setup script again:
```bash
cd /absolute/path/to/your/project
./scripts/setup-cursor-mcp.sh
```

## 📚 More Information

- **Detailed Setup:** See `CURSOR_SETUP.md`
- **Python CLI Usage:** See `QUICKSTART.md`
- **Test Results:** See `TEST_RESULTS.md`
- **General Setup:** See `SETUP_GUIDE.md`

## 🎉 You're All Set!

Your Cursor AI can now:
- ✅ Access your Microsoft Planner
- ✅ List your plans and buckets
- ✅ Create tasks through conversation
- ✅ Use your existing authentication

**Try it now:** Open Cursor and ask "What are my Planner plans?"

Enjoy seamless task management! 🚀
