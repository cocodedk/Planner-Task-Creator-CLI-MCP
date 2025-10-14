# Find Task Enhancements - Decisions

## D1: Naming Convention
**Choice**: Use explicit, purpose-driven names
- `get_task_details(task_id)` - fetch by known ID
- `find_task_by_title(title, plan_id)` - search by title
- Keep `resolve_task()` for backward compatibility

**Rationale**: 
- DRY: Reuse existing logic internally
- KISS: Clear names indicate purpose
- SOLID: Single responsibility per function

## D2: Function Signatures

### `get_task_details(task_id: str, token: str) -> dict`
**Parameters**:
- `task_id`: GUID only (validated with GUID_PATTERN)
- `token`: Access token
**Returns**: Full task object
**Raises**: ValueError if not found or invalid GUID

### `find_task_by_title(title: str, plan_id: str, token: str) -> dict`
**Parameters**:
- `title`: Task title (case-insensitive search)
- `plan_id`: Plan ID (required for scope)
- `token`: Access token
**Returns**: Single task object
**Raises**: ValueError with candidates if ambiguous or not found

## D3: Implementation Strategy
**Choice**: Wrapper functions around existing logic

```python
# New focused functions
def get_task_details(task_id, token):
    """Direct ID lookup - no plan needed."""
    if not GUID_PATTERN.match(task_id):
        raise ValueError("Invalid task ID format")
    return resolve_task(token, task_id, None)

def find_task_by_title(title, plan_id, token):
    """Title search within plan."""
    return resolve_task(token, title, plan_id)
```

**Rationale**:
- TAGNI: Don't duplicate logic unnecessarily
- KISS: Simple wrappers with clear interfaces
- MVP: Minimal code to deliver value

## D4: Module Organization
**Choice**: Keep in `task_operations.py`, add to barrel exports

**File Structure**:
```
planner_lib/
  task_operations.py      # Add new functions here (stays <100 lines)
  task_management.py      # Update exports
```

**Rationale**:
- Modularization: Related operations stay together
- File size: Adding ~20 lines keeps under 100-line guideline
- Composition: Reuse existing validated logic

## D5: CLI and MCP Exposure
**Choice**: No new CLI commands, no new MCP tools

**Rationale**:
- TAGNI: Existing `find-task-cmd` covers use cases
- KISS: Don't add redundant interfaces
- MVP: Python library API enhancement only

Users can import and use directly:
```python
from planner_lib import get_task_details, find_task_by_title
```

## D6: Backward Compatibility
**Choice**: Keep all existing functions unchanged

- `resolve_task()` stays public
- Existing CLI commands unchanged
- MCP tools unchanged
- Only adding, not modifying

