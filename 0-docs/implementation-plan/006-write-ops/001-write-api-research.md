# 006-write-ops/001: Write Operations API Research

## Goal
Identify Planner API endpoints for creating and updating tasks.

## Research Steps

1. **Create task manually in Planner UI**
   - Open DevTools Network tab
   - Create a new task in UI
   - Observe POST/PUT requests
   - Note endpoint, headers, payload

2. **Update task manually in Planner UI**
   - Change task title, due date, status
   - Observe API calls for each field
   - Note if different fields use different endpoints
   - Document payload format

3. **Identify required fields**
   - Which fields are required vs optional
   - Field validation rules
   - Field format requirements

4. **Test API calls from console**
   - Copy create task request as fetch
   - Test in console
   - Verify task appears in UI

5. **Document findings** in this file

## Deliverable

Update this document with:
```markdown
## Findings

### Create Task API
- Endpoint: [URL]
- Method: POST
- Headers: [required]
- Payload schema: [JSON structure]
- Required fields: [list]
- Optional fields: [list]

### Update Task API
- Endpoint: [URL]
- Method: PUT/PATCH
- Headers: [required]
- Payload schema: [JSON structure]
- Partial updates supported: yes/no

### Field Formats
- Title: [format]
- Due date: [ISO format, timezone handling]
- Status: [enum values]
- Assignee: [user ID format]
- Description: [format, length limit]

### Edge Cases Discovered
- [any quirks or gotchas]
```

## Acceptance Criteria

- [ ] Create task endpoint identified
- [ ] Update task endpoint identified
- [ ] Required vs optional fields documented
- [ ] Can create task from console
- [ ] Can update task from console

## ⚠️ File Size Reminder
**All source files created from this research must be under 200 lines. NO EXCEPTIONS.**

## Dependencies
- Completes after: 005-read-ops/005-read-ops-polish

## Time Estimate
2-3 hours (exploratory)

## Notes
Pay attention to validation errors. They reveal required formats and constraints.
