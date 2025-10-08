# 001-setup/004: Shared Types Package

## Goal
Create shared type definitions used by both extension and MCP server.

## Steps

1. **Create shared package structure**
   ```
   shared/
   ├── package.json
   ├── tsconfig.json
   ├── index.ts
   └── types/
       ├── planner.ts    # Planner domain types
       ├── messages.ts   # Message protocol types
       └── errors.ts     # Error types
   ```

2. **Define core Planner types** in `planner.ts`
   ```typescript
   - Plan (id, name, createdDate)
   - Task (id, title, dueDate, status, assignees, description)
   - Bucket (id, name, planId)
   - TaskStatus (NotStarted, InProgress, Completed)
   ```

3. **Define message protocol types** in `messages.ts`
   ```typescript
   - MessageType enum
   - Request/Response interfaces
   - Message payload types
   ```

4. **Define error types** in `errors.ts`
   ```typescript
   - OperationError interface
   - ErrorCode enum
   ```

5. **Create barrel export** in `index.ts`

6. **Configure as npm package**
   - `package.json` with `"type": "module"`
   - Export types from `package.json`

## Acceptance Criteria

- [ ] All type files created with core interfaces
- [ ] Barrel export configured
- [ ] Can import types in both extension and server
- [ ] **CRITICAL**: Each type file under 200 lines

## Dependencies
- Completes after: 001-project-structure

## Time Estimate
45 minutes

## Notes
Keep types minimal for MVP. Add only what's needed for CRUD operations.
