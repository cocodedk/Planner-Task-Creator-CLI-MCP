# Task Creation Module Specification

**Functions**:
- `parse_labels(labels_csv: Optional[str]) -> Dict[str, dict]`
- Task creation logic (integrated into CLI command)

**parse_labels Implementation**:
1. If labels_csv is None or empty, return `{}`
2. Split by comma and strip whitespace: `["Label1", "Label3"]`
3. Filter out empty strings
4. For each label, if it starts with "label" (case-insensitive):
   - Extract number: "label1" → 1, "Label2" → 2
   - Map to "category{number}": "category1", "category2"
   - Set value to `True`
5. Return dictionary like `{"category1": True, "category3": True}`

**Task Creation Process**:
1. Build payload with required fields:
   ```python
   payload = {
       "planId": plan_obj["id"],
       "bucketId": bucket_obj["id"],
       "title": title
   }
   ```
2. Add optional fields:
   - If due date: `"dueDateTime": f"{due}T17:00:00Z"`
   - If labels: `"appliedCategories": parse_labels(labels)`
   - If assignee: skip for now (can add user resolution later)

3. POST to `/planner/tasks`
4. Extract task ID from response
5. If description provided:
   - GET `/planner/tasks/{task_id}/details`
   - Extract `@odata.etag` from response
   - PATCH `/planner/tasks/{task_id}/details` with `{"description": desc}` and If-Match header

6. Return `{"taskId": task_id, "webUrl": task.get("detailsUrl", ""), "bucketId": bucket_obj["id"]}`

**Error Handling**: Graph API errors propagate up as HTTP errors from client module.
