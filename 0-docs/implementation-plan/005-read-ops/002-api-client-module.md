# 005-read-ops/002: Planner API Client Module

## Goal
Create API client module in extension for calling Planner endpoints.

## Steps

1. **Create API client structure**
   ```
   extension/src/content/api/
   ├── index.ts           # API client export
   ├── client.ts          # HTTP client wrapper
   ├── endpoints.ts       # Endpoint URLs and builders
   ├── parsers.ts         # Response parsers
   └── types.ts           # API-specific types
   ```

2. **Implement endpoints.ts** (<100 lines)
   - Endpoint URL constants/builders
   - Based on findings from 001-research
   - `buildPlansEndpoint()`
   - `buildTasksEndpoint(planId)`

3. **Implement client.ts** (<150 lines)
   ```typescript
   - makeRequest(endpoint, options)
   - Add required headers automatically
   - Use fetch API
   - Parse JSON responses
   - Wrap errors
   ```

4. **Implement parsers.ts** (<150 lines)
   ```typescript
   - parsePlansResponse(data)
   - parseTasksResponse(data)
   - Convert API format to shared types
   - Handle missing fields gracefully
   ```

5. **Create API method wrappers**
   ```typescript
   - getPlans(): Promise<Plan[]>
   - getTasks(planId: string): Promise<Task[]>
   - Each calls client, parses response
   ```

6. **Error handling**
   - Network errors
   - Parse errors
   - API errors (4xx, 5xx)
   - Return structured errors

## Acceptance Criteria

- [ ] API client can call Planner endpoints
- [ ] Responses parsed to shared types
- [ ] Errors handled and wrapped
- [ ] Can call from content script
- [ ] All files under 200 lines

## Dependencies
- Completes after: 005-read-ops/001-planner-api-research

## Time Estimate
2 hours

## DRY Notes
- Reuse shared error types from `shared/`
- Reuse retry logic from extension utilities
- Extract repeated parsing logic
