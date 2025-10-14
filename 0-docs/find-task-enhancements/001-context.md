# Find Task Enhancements - Context

## Current State

### Existing Functionality
- **`resolve_task()`**: Finds task by GUID or title (case-insensitive)
  - Location: `planner_lib/task_operations.py:51-99`
  - Takes: `token`, `task` (ID/title), `plan_id` (optional for GUID)
  - Returns: Full task object
  - Errors: Ambiguous matches, not found

- **`find_task_cmd`**: CLI wrapper for `resolve_task()`
  - Location: `planner_lib/cli_task_list.py:63-112`
  - Command: `planner find-task-cmd --task "X" [--plan "Y"]`
  - MCP Tool: `planner_findTask`

### Current Limitations
1. No dedicated API for finding by title without plan context
2. Function name `resolve_task` doesn't clearly indicate search capability
3. No explicit "get task details by ID" function (buried in resolve logic)
4. Ambiguous naming - "resolve" vs "find" vs "get"

## Proposed New Features

### 1. `find_task_by_title(title, board_name)`
**Purpose**: Explicit title-based search with clear naming
- Search for task by title within a specific plan
- Return single match or candidates if ambiguous
- Clear separation from ID-based lookup

### 2. `get_task_details(task_id)`
**Purpose**: Direct GUID-based task retrieval
- Fetch full task object by known task ID
- Simpler interface when ID is already known
- No plan context required

## Problem Statement
Users need:
- Clear, intuitive function names that match intent
- Separate functions for "I have an ID" vs "I need to find by title"
- Consistent naming with other operations (get, list, find)

## Success Criteria
- New functions coexist with existing `resolve_task()`
- No breaking changes to current CLI/MCP tools
- Clear documentation of when to use each function
- File size stays under 100 lines per module guideline

