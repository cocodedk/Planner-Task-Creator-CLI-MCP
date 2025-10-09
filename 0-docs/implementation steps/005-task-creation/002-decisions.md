# Task Creation Module Decisions

**Label Format**: Parse CSV like "Label1,Label3" into Graph API category format.

**Label Mapping**: Map "Label1" → "category1", "Label2" → "category2", etc.

**Date Format**: Convert "YYYY-MM-DD" to ISO format "YYYY-MM-DDTHH:MM:SSZ" (use 17:00:00 UTC).

**Description Handling**: Two-step process - create task, then PATCH details with ETag.

**Assignment Handling**: For now, skip user ID resolution (let Graph handle UPN). Can be added later if needed.

**API Endpoints**:
- Create: `POST /planner/tasks`
- Details: `GET /planner/tasks/{id}/details` then `PATCH /planner/tasks/{id}/details`

**Response Format**: Return `{"taskId": "...", "webUrl": "...", "bucketId": "..."}`
