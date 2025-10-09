# Examples: Microsoft Planner Task Creator CLI

This document provides practical examples for common use cases.

## 📚 Table of Contents

- [Basic Usage](basic-usage.md) - First-time setup and getting started
- [Authentication](authentication.md) - Authentication flows and configuration
- [Configuration](configuration.md) - Setting up defaults and preferences
- [Task Creation](task-creation.md) - Creating tasks with various options
- [Listing and Discovery](listing-discovery.md) - Finding plans, buckets, and tasks
- [Advanced Scenarios](advanced-scenarios.md) - Scripting, automation, and batch operations
- [Shell Integration](shell-integration.md) - Shell aliases and integration
- [MCP Server Usage](mcp-server-usage.md) - Using with AI assistants

## 🎯 Quick Examples

### Create a Task
```bash
python planner.py add --title "Review code" --due "2024-12-31"
```

### List Plans
```bash
python planner.py list-plans
```

### Set Defaults
```bash
python planner.py set-defaults --plan "Work" --bucket "To Do"
```

## 🔧 Common Workflows

- **Daily tasks**: Create tasks for today's work
- **Project management**: Organize tasks by project and priority
- **Team coordination**: Share task status and assignments
- **Personal productivity**: Track personal goals and deadlines

## 🚀 Advanced Usage

- **Automation scripts**: Create tasks from CSV files or APIs
- **Integration**: Connect with other tools and services
- **Custom workflows**: Build scripts for specific use cases
