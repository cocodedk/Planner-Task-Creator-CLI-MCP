# 010 - Task Management Operations

## Problem
Current MCP cannot:
- Find/list existing tasks
- Update task properties
- Mark tasks complete
- Move tasks between buckets
- Split tasks into subtasks

## Goal
Add task lifecycle management to CLI and MCP.

## Scope - Phase 1: Read Operations
- List tasks (by plan/bucket)
- Find task by title
- Get task details

## Scope - Phase 2: Update Operations
- Update task fields
- Mark complete
- Move to bucket

## Scope - Phase 3: Checklist Operations
- Add checklist items
- Complete checklist items
- List checklist items

## Scope - Phase 4: Delete Operations
- Delete task (with safety flag)

## Out of Scope
- Task assignments
- Priority changes
- Cross-plan moves
- Comments/attachments
- Bulk operations

## Success Metrics
- Can find task by title in <2s
- Update operations succeed with auto-retry on ETag conflict
- All operations available in MCP tools
