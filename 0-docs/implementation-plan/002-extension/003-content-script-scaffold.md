# 002-extension/003: Content Script Scaffold

## Goal
Create content script that runs on Planner pages with DOM detection.

## Steps

1. **Create content module structure**
   ```
   extension/src/content/
   ├── index.ts           # Entry point, initialization
   ├── messaging.ts       # Communication with background
   ├── plannerDetect.ts   # Detect Planner UI state
   ├── constants.ts       # Selectors, URLs
   └── types.ts           # Content-specific types
   ```

2. **Implement index.ts**
   - Wait for DOM ready
   - Initialize messaging connection
   - Call planner detection
   - Log initialization success

3. **Implement plannerDetect.ts**
   - `isPlannerPage()`: Check URL and DOM
   - `waitForPlannerLoad()`: Wait for UI ready
   - `getPlannerContext()`: Extract current plan/task from URL/DOM

4. **Implement constants.ts**
   - Planner URL patterns
   - Common CSS selectors (minimal set for detection)
   - Timeout values

5. **Implement messaging.ts**
   - Send message to background helper
   - Receive and handle background messages
   - Connection management

## Acceptance Criteria

- [ ] Content script loads on Planner pages only
- [ ] Can detect when Planner UI is ready
- [ ] Can communicate with background script
- [ ] Logs show successful initialization
- [ ] All files under 200 lines

## Dependencies
- Completes after: 002-extension/002-background-scaffold

## Time Estimate
1.5 hours

## Testing Notes
- Manually load extension in Chrome
- Navigate to tasks.office.com
- Check console for initialization logs
- Verify message passing with background
