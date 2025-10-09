# Update Task Labels - Context

## Problem

Users cannot add, remove, or modify labels on existing tasks. Labels can only be set when creating new tasks.

## Use Cases

1. **Add labels to existing tasks** - Apply categories to tasks after creation
2. **Remove labels from tasks** - Clear categories that are no longer relevant
3. **Change task labels** - Replace existing labels with new ones
4. **Bulk categorization** - Apply labels to tasks as workflows evolve

## Current Limitations

- ✅ Can add labels during task creation
- ❌ Cannot update labels on existing tasks
- ❌ Cannot remove labels from tasks
- ❌ No general task property update command

## Goal

Add functionality to update task labels after creation via CLI, MCP, and Python API.

## Success Criteria

- Update labels on existing task by title or ID
- Support add, remove, and replace operations
- Include proper ETag handling for concurrency
- Available in CLI, MCP, and Python API
- Full test coverage
- Documentation and examples
