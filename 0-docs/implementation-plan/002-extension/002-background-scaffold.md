# 002-extension/002: Background Script Scaffold

## Goal
Create background service worker with message routing foundation.

## Steps

1. **Create background module structure**
   ```
   extension/src/background/
   ├── index.ts           # Entry point, lifecycle
   ├── messaging.ts       # Message routing
   ├── handlers.ts        # Message handlers
   └── types.ts           # Background-specific types
   ```

2. **Implement index.ts**
   - Service worker lifecycle (install, activate)
   - Initialize message listeners
   - Basic logging setup

3. **Implement messaging.ts**
   - `onMessage` listener setup
   - Message routing by type
   - Response handling

4. **Implement handlers.ts** (stubs)
   - Handler function signatures
   - Return mock responses for now
   - Error handling wrapper

5. **Define types.ts**
   - MessageHandler type
   - HandlerContext interface
   - Response types

## Acceptance Criteria

- [ ] Background script loads without errors
- [ ] Message routing infrastructure in place
- [ ] Can receive and respond to test messages
- [ ] All files under 200 lines
- [ ] Logging shows lifecycle events

## Dependencies
- Completes after: 001-setup/004-shared-types, 002-extension/001-manifest-setup

## Time Estimate
1 hour

## Architecture Notes
- Single Responsibility: Each handler in handlers.ts does ONE operation
- Messaging.ts only routes, never implements business logic
- All shared types imported from `shared/`
