# 007-delete-ops/001: Delete Operation API Research

## Goal
Identify Planner API endpoint for deleting tasks and safety mechanisms.

## Research Steps

1. **Delete task manually in Planner UI**
   - Open DevTools Network tab
   - Delete a task in UI
   - Observe DELETE/POST request
   - Note endpoint, headers, payload

2. **Check for confirmation mechanisms**
   - Does UI show confirmation dialog?
   - Is there an undo mechanism?
   - Can deleted tasks be recovered?

3. **Test API call from console**
   - Copy delete request as fetch
   - Test on a test task
   - Verify task disappears

4. **Research soft delete vs hard delete**
   - Is deletion immediate?
   - Are tasks moved to trash first?
   - Can deletion be undone via API?

5. **Document findings** in this file

## Deliverable

Update this document with:
```markdown
## Findings

### Delete Task API
- Endpoint: [URL]
- Method: DELETE
- Headers: [required]
- Payload: [if any]
- Response: [structure]

### Safety Mechanisms
- Soft delete: yes/no
- Trash/recycle bin: yes/no
- Undo API: yes/no
- Confirmation required: yes/no

### Risks
- [any data loss risks]
- [recovery mechanisms]
```

## Acceptance Criteria

- [ ] Delete endpoint identified
- [ ] Safety mechanisms understood
- [ ] Can delete task from console
- [ ] Verified task disappears from UI
- [ ] Recovery options documented

## ⚠️ File Size Reminder
**All source files created must be under 200 lines. NO EXCEPTIONS.**

## Dependencies
- Completes after: 006-write-ops/004-write-ops-polish

## Time Estimate
1 hour

## Safety Note
Test on dummy tasks only. Document any recovery mechanisms discovered.
