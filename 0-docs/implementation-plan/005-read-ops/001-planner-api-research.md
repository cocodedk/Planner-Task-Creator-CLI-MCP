# 005-read-ops/001: Planner API Research & Discovery

## Goal
Identify how to retrieve plans and tasks from Planner web UI.

## Approach Options

### Option A: DOM Scraping
- Parse rendered HTML for task data
- Pro: Simple, no auth needed
- Con: Fragile, UI changes break it

### Option B: Network Interception
- Intercept XHR/fetch calls to Microsoft APIs
- Pro: Gets structured data
- Con: May have CORS issues

### Option C: Internal API Calls
- Reverse engineer API endpoints
- Call them directly from extension
- Pro: Structured data, no DOM parsing
- Con: May change, authentication needed

## Research Steps

1. **Open Planner in browser with DevTools**
   - Go to tasks.office.com
   - Open Network tab
   - Observe API calls when loading plans/tasks

2. **Identify key endpoints**
   - List plans endpoint
   - Get tasks for plan endpoint
   - Request/response formats
   - Authentication headers

3. **Test API calls from console**
   - Copy request as fetch
   - Test in console
   - Verify response structure

4. **Document findings** in this file
   - API endpoints
   - Required headers
   - Authentication mechanism
   - Request/response schemas

## Deliverable

Update this document with:
```markdown
## Findings

### Plans List API
- Endpoint: [URL]
- Method: GET/POST
- Headers: [required headers]
- Response: [structure]

### Tasks List API
- Endpoint: [URL]
- Method: GET/POST
- Headers: [required headers]
- Query params: [planId, etc.]
- Response: [structure]

### Authentication
- Mechanism: [cookies/bearer token/etc.]
- Where to get: [from browser session]
```

## Acceptance Criteria

- [ ] Plans API endpoint identified
- [ ] Tasks API endpoint identified
- [ ] Authentication mechanism understood
- [ ] Can successfully call APIs from console
- [ ] Response schema documented

## ⚠️ File Size Reminder
**All source files created from this research must be under 200 lines. NO EXCEPTIONS.**

## Dependencies
- Completes after: 002-extension/003-content-script-scaffold

## Time Estimate
2-3 hours (exploratory)

## Notes
This is exploratory. Take notes as you go. The findings drive next steps.
