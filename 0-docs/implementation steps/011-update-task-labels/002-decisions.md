# Update Task Labels - Decisions

## API Approach

**Decision**: Use `PATCH /planner/tasks/{task-id}` with ETag
**Rationale**: Standard approach for updating task properties, requires optimistic concurrency control

## Update Modes

**Decision**: Support label replacement (not merge)
**Rationale**:
- Simple and predictable behavior
- Matches task creation pattern
- User specifies complete desired label set
- Can remove labels by omitting them

**Alternative Considered**: Add/remove modes (--add-labels, --remove-labels)
**Rejected**: More complex, harder to reason about, can achieve same result with replacement

## Label Format

**Decision**: Reuse existing CSV format "Label1,Label3"
**Rationale**: Consistent with task creation, familiar to users

## Task Resolution

**Decision**: Support both title and ID lookup
**Rationale**: Matches existing pattern in other task operations (complete, move, delete)

## CLI Command Name

**Decision**: `update-task --task "..." --labels "Label1,Label3"`
**Rationale**:
- Extensible for future task updates (due date, title, etc.)
- Clear and discoverable
- Follows existing command patterns

## MCP Tool Name

**Decision**: `planner_updateTask`
**Rationale**: Matches naming convention of other tools

## Empty Labels Handling

**Decision**: Empty string or no labels parameter = clear all labels
**Rationale**: Provides way to remove all labels from a task

## ETag Conflict Handling

**Decision**: Automatic retry on 412 Precondition Failed
**Rationale**: Matches existing pattern in graph_client.py, handles concurrent updates gracefully
