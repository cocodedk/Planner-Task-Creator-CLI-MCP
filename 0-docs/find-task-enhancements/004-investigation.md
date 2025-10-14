# Investigation - Find Task Enhancements

## Current Architecture Analysis

### Function Call Flow
```
User Code
  ↓
find_task_by_title() ──→ resolve_task() ──→ list_tasks() → Graph API
                                         ├─→ case_insensitive_match()
                                         └─→ error formatting

get_task_details() ──────→ get_json() ──→ Graph API /planner/tasks/{id}
```

### Code Duplication Risk
**Current**: `resolve_task()` has two paths:
1. GUID → direct fetch (7 lines)
2. Title → search (21 lines)

**Risk**: New functions might duplicate error handling

**Mitigation**: Wrapper pattern reuses existing logic:
- `get_task_details()` validates GUID, calls Graph API directly
- `find_task_by_title()` delegates search logic to existing code

### File Size Analysis
**Current `task_operations.py`**: 99 lines
- Imports/constants: 12 lines
- `list_tasks()`: 35 lines
- `resolve_task()`: 49 lines
- Empty lines/docstrings: 3 lines

**After Changes**: ~150 lines
- `get_task_details()`: ~25 lines (with docstring)
- `find_task_by_title()`: ~30 lines (with docstring)

**Decision**: Acceptable for now. If grows beyond 150, split:
```
task_operations/
  __init__.py          # Barrel exports
  list.py              # list_tasks
  resolve.py           # resolve_task (legacy)
  get_details.py       # get_task_details
  find_by_title.py     # find_task_by_title
```

## Dependencies

### Required Imports (already present)
- `json` - error formatting
- `typing.Optional, List` - type hints
- `.constants.BASE_GRAPH_URL, GUID_PATTERN` - validation
- `.graph_client.get_json` - API calls
- `.resolution_utils.case_insensitive_match` - title matching

**No new dependencies needed** ✓

### Impact on Other Modules
**Zero impact** - only additions:
- `task_management.py` - add exports (2 lines)
- `__init__.py` - add public API (2 lines)

## Error Handling Consistency

### Current Pattern
```python
raise ValueError(json.dumps({
    "code": "ErrorType",
    "message": "Description",
    "candidates": [...]  # optional
}))
```

### New Functions Follow Same Pattern
- `InvalidTaskId` - for malformed GUIDs
- `TaskNotFound` - for 404s
- `AmbiguousTask` - for multiple matches

**Consistency**: ✓ Matches existing error format

## Testing Strategy

### Mock Requirements
- `get_json()` - mock Graph API responses
- `list_tasks()` - mock task lists
- `GUID_PATTERN` - use real regex (no mock needed)

### Test Data
```python
MOCK_TASK_ID = "8bc07d47-c06f-459f-b97e-49c4d6a1b042"
MOCK_PLAN_ID = "plan123"
MOCK_TASK = {
    "id": MOCK_TASK_ID,
    "title": "Test Task",
    "bucketId": "bucket123",
    "percentComplete": 0
}
```

### Edge Cases
1. Empty title string
2. Special characters in title
3. Very long titles (>255 chars)
4. Unicode in titles
5. Network timeout (API errors)
6. Invalid JSON responses

## Backward Compatibility

### Breaking Changes: NONE
- All existing functions unchanged
- All existing CLI commands unchanged
- All existing MCP tools unchanged

### Deprecation Path: NONE
- `resolve_task()` stays public
- May add "prefer get_task_details/find_task_by_title" to docs
- No timeline for removal

## Performance Considerations

### Network Calls
- `get_task_details()`: 1 API call (same as resolve_task with GUID)
- `find_task_by_title()`: 2 API calls (list + match, same as resolve_task with title)

**No performance regression** ✓

### Memory Usage
- Minimal - small wrapper functions
- No additional caching needed

## Security Considerations

### Input Validation
- `task_id`: GUID regex validation prevents injection
- `title`: String comparison only, no eval/exec
- `plan_id`: Passed to validated Graph API

**No new security risks** ✓

### API Permissions
- Same permissions as existing `resolve_task()`
- Requires `Tasks.ReadWrite` Graph API scope

## Documentation Requirements

### Code Documentation
- Docstrings with Args/Returns/Raises (included in implementation)
- Type hints (included in implementation)

### User Documentation
- Update README with new function examples
- Add to API reference (if exists)
- Update architecture docs (optional)

### Developer Documentation
- This investigation doc serves as design reference
- Implementation plan has code examples
- Tests serve as usage examples

