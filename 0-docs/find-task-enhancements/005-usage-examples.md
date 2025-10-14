# Usage Examples - Find Task Enhancements

## Python Library Usage

### Import the Functions

```python
from planner_lib import get_task_details, find_task_by_title
# Or import from specific module
from planner_lib.task_operations import get_task_details, find_task_by_title
```

### Get Task Details by ID

When you already have a task ID (GUID):

```python
from planner_lib import get_task_details, get_tokens

# Authenticate
token = get_tokens(tenant_id, client_id)

# Fetch task by ID
task_id = "8bc07d47-c06f-459f-b97e-49c4d6a1b042"
task = get_task_details(task_id, token)

print(f"Task: {task['title']}")
print(f"Progress: {task['percentComplete']}%")
print(f"Bucket: {task['bucketId']}")
```

**Error Handling:**
```python
import json

try:
    task = get_task_details("invalid-id", token)
except ValueError as e:
    error = json.loads(str(e))
    if error["code"] == "InvalidTaskId":
        print("Task ID format is invalid")
    elif error["code"] == "NotFound":
        print("Task not found")
```

### Find Task by Title

When you need to search for a task by its title:

```python
from planner_lib import find_task_by_title, resolve_plan, get_tokens

# Authenticate
token = get_tokens(tenant_id, client_id)

# Get plan ID
plan = resolve_plan(token, "My Project")
plan_id = plan["id"]

# Find task by title (case-insensitive)
task = find_task_by_title("Fix login bug", plan_id, token)

print(f"Found task: {task['title']}")
print(f"Task ID: {task['id']}")
```

**Error Handling:**
```python
import json

try:
    task = find_task_by_title("Bug Fix", plan_id, token)
except ValueError as e:
    error = json.loads(str(e))
    
    if error["code"] == "AmbiguousTask":
        print("Multiple tasks match:")
        for candidate in error["candidates"]:
            print(f"  - {candidate['title']} (ID: {candidate['id']})")
            
    elif error["code"] == "TaskNotFound":
        print(f"Task not found. Similar tasks:")
        for candidate in error["candidates"][:5]:
            print(f"  - {candidate['title']}")
```

## Comparison with `resolve_task()`

### Old Way (still works)
```python
from planner_lib import resolve_task

# Ambiguous - is this an ID or title?
task = resolve_task(token, some_identifier, plan_id)
```

### New Way (clearer intent)
```python
from planner_lib import get_task_details, find_task_by_title

# Clear: fetching by ID
task = get_task_details(task_id, token)

# Clear: searching by title
task = find_task_by_title(title, plan_id, token)
```

## When to Use Each Function

### Use `get_task_details(task_id, token)`
- ✅ You have a task ID from a previous operation
- ✅ You need to refresh task data
- ✅ You're building APIs where IDs are standard
- ✅ No plan context is available

### Use `find_task_by_title(title, plan_id, token)`
- ✅ You know the task title
- ✅ You're building user-facing features
- ✅ You want explicit search semantics
- ✅ Plan context is readily available

### Use `resolve_task(token, task, plan_id)` (legacy)
- ✅ You need backward compatibility
- ✅ Input could be either ID or title
- ✅ You're maintaining existing code

## Integration Examples

### Workflow: Create → Get Details
```python
from planner_lib import create_task, get_task_details, get_tokens

token = get_tokens(tenant_id, client_id)

# Create task
result = create_task(
    token=token,
    plan_id=plan_id,
    bucket_id=bucket_id,
    title="New Feature"
)

# Get full details
task = get_task_details(result["taskId"], token)
print(f"Created: {task['title']}")
```

### Workflow: Find by Title → Update
```python
from planner_lib import find_task_by_title, complete_task_op

# Find task
task = find_task_by_title("Deploy to production", plan_id, token)

# Mark complete
complete_task_op(task["id"], token)
```

### Workflow: Bulk Operations
```python
from planner_lib import find_task_by_title, get_task_details

task_titles = ["Bug #1", "Bug #2", "Bug #3"]
tasks = []

for title in task_titles:
    try:
        task = find_task_by_title(title, plan_id, token)
        tasks.append(task)
    except ValueError as e:
        error = json.loads(str(e))
        if error["code"] == "TaskNotFound":
            print(f"Skipping: {title} not found")

# Process found tasks
for task in tasks:
    details = get_task_details(task["id"], token)
    print(f"{details['title']}: {details['percentComplete']}%")
```

## Performance Considerations

### Network Calls
- `get_task_details()`: 1 API call
- `find_task_by_title()`: 2 API calls (list + match)

### Best Practices
```python
# ❌ Don't repeatedly search by title
for i in range(100):
    task = find_task_by_title("Same Task", plan_id, token)  # Wasteful

# ✅ Search once, cache ID
task = find_task_by_title("Task", plan_id, token)
task_id = task["id"]
for i in range(100):
    task = get_task_details(task_id, token)  # Efficient
```

## Error Reference

### `get_task_details()` Errors
- `InvalidTaskId`: Task ID format invalid (not a GUID)
- `NotFound`: Task ID not found in Graph API

### `find_task_by_title()` Errors
- `AmbiguousTask`: Multiple tasks with same title (includes candidates)
- `TaskNotFound`: No task matches title (includes up to 5 similar tasks)

## Type Hints

Both functions are fully typed:

```python
def get_task_details(task_id: str, token: str) -> dict:
    ...

def find_task_by_title(title: str, plan_id: str, token: str) -> dict:
    ...
```

Use with mypy or other type checkers for enhanced safety.

