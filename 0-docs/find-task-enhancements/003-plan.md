# Find Task Enhancements - Implementation Plan

## Overview
Add two focused functions to `planner_lib/task_operations.py` that provide clear, purpose-specific interfaces for task lookup.

## Implementation Steps

### Step 1: Add New Functions to `task_operations.py`
**File**: `planner_lib/task_operations.py`

Add after existing `resolve_task()` function:

```python
def get_task_details(task_id: str, token: str) -> dict:
    """
    Fetch task details by task ID.
    
    Args:
        task_id: Task GUID
        token: Access token
        
    Returns:
        Full task object
        
    Raises:
        ValueError: If task_id invalid format or task not found
    """
    if not GUID_PATTERN.match(task_id):
        raise ValueError(json.dumps({
            "code": "InvalidTaskId",
            "message": f"Invalid task ID format: {task_id}"
        }))
    
    url = f"{BASE_GRAPH_URL}/planner/tasks/{task_id}"
    return get_json(url, token)


def find_task_by_title(title: str, plan_id: str, token: str) -> dict:
    """
    Find task by title within a plan.
    
    Args:
        title: Task title (case-insensitive)
        plan_id: Plan ID to search within
        token: Access token
        
    Returns:
        Task object if single match found
        
    Raises:
        ValueError: With candidates if ambiguous or not found
    """
    tasks = list_tasks(token, plan_id=plan_id)
    matches = case_insensitive_match(tasks, "title", title)
    
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        candidates = [{"id": t["id"], "title": t["title"], "bucketId": t.get("bucketId", "")}
                     for t in matches]
        raise ValueError(json.dumps({
            "code": "AmbiguousTask",
            "message": f"Multiple tasks match '{title}'",
            "candidates": candidates
        }))
    else:
        candidates = [{"id": t["id"], "title": t["title"]} for t in tasks[:5]]
        raise ValueError(json.dumps({
            "code": "TaskNotFound",
            "message": f"Task '{title}' not found",
            "candidates": candidates
        }))
```

**Lines Added**: ~50 (file stays under 150 total)

### Step 2: Update Barrel Exports
**File**: `planner_lib/task_management.py`

Add to imports and `__all__`:
```python
from .task_operations import list_tasks, resolve_task, get_task_details, find_task_by_title

__all__ = [
    "list_tasks",
    "resolve_task",
    "get_task_details",      # NEW
    "find_task_by_title",    # NEW
    ...
]
```

### Step 3: Update Package Exports
**File**: `planner_lib/__init__.py`

Add to public API:
```python
from .task_management import (
    ...,
    get_task_details,
    find_task_by_title,
)
```

### Step 4: Add Unit Tests
**File**: `tests/test_task_operations/test_task_find_enhancements.py` (new)

Test cases:
- `test_get_task_details_valid_id()` - Success case
- `test_get_task_details_invalid_format()` - Invalid GUID
- `test_get_task_details_not_found()` - 404 error
- `test_find_task_by_title_single_match()` - Success case
- `test_find_task_by_title_ambiguous()` - Multiple matches
- `test_find_task_by_title_not_found()` - No matches
- `test_find_task_by_title_case_insensitive()` - Case handling

### Step 5: Update Documentation
**File**: `docs/PROJECT_SUMMARY/task-operations.md` (if exists)

Document new functions with examples:
```python
# Direct ID lookup
task = get_task_details("abc-123-def", token)

# Title search
task = find_task_by_title("Fix login bug", plan_id, token)
```

## File Size Summary
- `task_operations.py`: 99 → ~150 lines (needs split if >150)
- `task_management.py`: 19 → 21 lines ✓
- New test file: ~100 lines ✓

## Verification Steps
1. Run `pytest tests/test_task_operations/` - all pass
2. Import new functions in Python REPL
3. Check file sizes comply with <100 line guideline
4. Verify backward compatibility - existing tests still pass

