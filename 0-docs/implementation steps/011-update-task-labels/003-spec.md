# Update Task Labels - Specification

## Python API

### Function: `update_task_labels()`

**Location**: `planner_lib/task_update_labels.py`

**Signature**:
```python
def update_task_labels(
    task_id: str,
    labels: Optional[str],
    token: str
) -> dict:
    """
    Update labels on an existing task.

    Args:
        task_id: Task ID (GUID)
        labels: Comma-separated labels like "Label1,Label3" or None to clear
        token: Access token

    Returns:
        Updated task object
    """
```

**Implementation**:
1. Parse labels using existing `parse_labels()` function
2. GET task to retrieve current ETag: `GET /planner/tasks/{task_id}`
3. Extract `@odata.etag` from response
4. Build PATCH payload: `{"appliedCategories": parsed_labels}`
5. PATCH with If-Match header: `PATCH /planner/tasks/{task_id}`
6. Return updated task object

**ETag Handling**: Use existing `patch_json()` which handles retry on 412

## CLI Command

### Command: `update-task`

**Location**: `planner_lib/cli_task_update.py` (extend existing)

**Usage**:
```bash
python planner.py update-task \
  --task "Task Title or ID" \
  --plan "Plan Name" \
  --labels "Label1,Label3"
```

**Parameters**:
- `--task` (required): Task title or ID
- `--plan` (optional): Plan name or ID (for title resolution)
- `--labels` (optional): Comma-separated labels, empty string to clear

**Process**:
1. Load config for auth
2. Resolve task by title or ID using existing `resolve_task()`
3. Call `update_task_labels()`
4. Output JSON result

## MCP Tool

### Tool: `planner_updateTask`

**Location**: `src/server/handlers-tasks.ts`

**Input Schema**:
```typescript
{
  task: string;      // Task title or ID (required)
  plan?: string;     // Plan name or ID (for title resolution)
  labels?: string;   // "Label1,Label3" or empty to clear
}
```

**Handler**: `handleUpdateTask()`

**Process**:
1. Build CLI args: `["update-task", "--task", task]`
2. Add `--plan` if provided
3. Add `--labels` if provided
4. Execute CLI via `runCli()`
5. Parse and return result

## Tool Definition

**Location**: `src/server/tools.ts`

```typescript
{
  name: "planner_updateTask",
  description: "Update labels on an existing task",
  inputSchema: {
    type: "object",
    properties: {
      task: {
        type: "string",
        description: "Task title or ID (required)"
      },
      plan: {
        type: "string",
        description: "Plan name or ID (required for title-based search)"
      },
      labels: {
        type: "string",
        description: "Comma-separated labels like 'Label1,Label3' (empty to clear)"
      }
    },
    required: ["task"]
  }
}
```

## Error Handling

**Task Not Found**: Return JSON error via existing resolution mechanism
**Invalid Labels**: Silently filter (matches creation behavior)
**ETag Conflict**: Automatic retry via `patch_json()`
**API Errors**: Propagate HTTP errors with structured JSON

## Testing

### Unit Tests

**Location**: `tests/test_task_update_labels.py`

**Test Cases**:
1. `test_update_task_labels_add()` - Add labels to task
2. `test_update_task_labels_replace()` - Replace existing labels
3. `test_update_task_labels_clear()` - Clear all labels (empty string)
4. `test_update_task_labels_single()` - Update with single label
5. `test_update_task_labels_multiple()` - Update with multiple labels
6. `test_update_task_labels_etag_retry()` - Verify ETag handling

### Integration Tests

**Manual Testing**:
```bash
# Add labels to task
python planner.py update-task \
  --task "My Task" \
  --plan "Test Plan" \
  --labels "Label1,Label2"

# Clear labels
python planner.py update-task \
  --task "My Task" \
  --plan "Test Plan" \
  --labels ""
```

## API Reference

### Microsoft Graph Endpoint

```http
PATCH https://graph.microsoft.com/v1.0/planner/tasks/{task-id}
If-Match: W/"JzEtVGFzayAgQEBA..."
Content-Type: application/json

{
  "appliedCategories": {
    "category1": true,
    "category3": true
  }
}
```

**Response**: Updated task object with new ETag

## Examples

### CLI Examples

```bash
# Add labels to task
python planner.py update-task \
  --task "Fix bug" \
  --plan "Dev Sprint" \
  --labels "Label1,Label3"

# Replace labels
python planner.py update-task \
  --task "Feature work" \
  --labels "Label2"

# Clear all labels
python planner.py update-task \
  --task "Old task" \
  --labels ""
```

### MCP Examples

```typescript
// Add labels
await mcp.call("planner_updateTask", {
  task: "Review PR",
  plan: "Dev Sprint",
  labels: "Label1,Label2"
});

// Clear labels
await mcp.call("planner_updateTask", {
  task: "Old Task",
  plan: "Archive",
  labels: ""
});
```

### Python API Examples

```python
from planner_lib.task_update_labels import update_task_labels

# Update labels
result = update_task_labels(
    task_id="task-guid-123",
    labels="Label1,Label3",
    token=token
)

# Clear labels
result = update_task_labels(
    task_id="task-guid-456",
    labels="",
    token=token
)
```
