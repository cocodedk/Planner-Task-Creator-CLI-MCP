# 010 - Implementation Plan

## Effort Estimate
- **Total**: ~8-12 hours
- **Per phase**: 2-3 hours each

## Phase 1: Read Operations (2-3h)
**Files to modify:**
- `planner.py`: Add `list_tasks()`, `resolve_task()`
- `planner.py`: Add CLI commands `list-tasks`, `find-task`
- `src/server.ts`: Add MCP tools
- `tests/`: Add test cases

**Order:**
1. Implement `list_tasks()` function
2. Add `list-tasks` CLI command
3. Implement `resolve_task()` function
4. Test both functions
5. Add MCP tools for both
6. Test MCP integration

## Phase 2: Update Operations (2-3h)
**Files to modify:**
- `planner.py`: Add `complete_task_op()`, `move_task_op()`
- `planner.py`: Add CLI commands
- `src/server.ts`: Add MCP tools
- `tests/`: Add test cases

**Order:**
1. Implement complete operation
2. Test with various task states
3. Implement move operation
4. Test bucket resolution
5. Add MCP tools
6. Test end-to-end

## Phase 3: Subtasks (2-3h)
**Files to modify:**
- `planner.py`: Add `add_subtask()`, `list_subtasks()`, `complete_subtask()`
- `planner.py`: Add CLI commands (3)
- `src/server.ts`: Add MCP tools (3)
- `tests/`: Add test cases

**Order:**
1. Implement add_subtask with GUID generation
2. Implement list_subtasks
3. Implement complete_subtask with title resolution
4. Test checklist operations
5. Add all MCP tools
6. Test integration

## Phase 4: Delete (1-2h)
**Files to modify:**
- `planner.py`: Add `delete_task()`, add CLI command
- `src/server.ts`: Add MCP tool
- `tests/`: Add test cases

**Order:**
1. Implement delete with ETag
2. Add --confirm flag logic
3. Test safety mechanisms
4. Add MCP tool (no confirm needed)
5. Test both paths

## Module Structure (Keep Files Small)
All functions stay in `planner.py` but grouped:
- Lines 1-300: Existing (auth, config, graph, resolution, create)
- Lines 301-400: Task operations (list, find, complete, move, delete)
- Lines 401-500: Checklist operations (add, list, complete)
- Lines 501-700: CLI commands (existing + new)

Keep each function <30 lines, following modularization rules.

## Testing Strategy
- Unit tests for each function
- Integration tests for CLI commands
- MCP tool tests via test script
- Manual E2E test with real Planner
