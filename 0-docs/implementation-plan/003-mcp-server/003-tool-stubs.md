# 003-mcp-server/003: Tool Implementation Stubs

## Goal
Create stub implementations for all five MVP tools.

## Steps

1. **Create tool files**
   ```
   mcp-server/src/tools/
   ├── getPlans.ts
   ├── getTasks.ts
   ├── createTask.ts
   ├── updateTask.ts
   └── deleteTask.ts
   ```

2. **Implement each tool stub** (each file <100 lines)
   - Import shared types
   - Define input interface
   - Define output interface
   - Export handler function
   - Return mock data for now

3. **getPlans.ts stub**
   ```typescript
   - Input: none
   - Output: Plan[]
   - Mock: Return 2-3 dummy plans
   ```

4. **getTasks.ts stub**
   ```typescript
   - Input: { planId: string }
   - Output: Task[]
   - Mock: Return 3-5 dummy tasks
   ```

5. **createTask.ts stub**
   ```typescript
   - Input: { planId, title, dueDate?, assignee?, description? }
   - Output: Task
   - Mock: Return created task with generated ID
   ```

6. **updateTask.ts stub**
   ```typescript
   - Input: { taskId, updates: Partial<Task> }
   - Output: Task
   - Mock: Return merged task
   ```

7. **deleteTask.ts stub**
   ```typescript
   - Input: { taskId }
   - Output: { success: boolean }
   - Mock: Return success
   ```

8. **Register all tools** in tools/index.ts

## Acceptance Criteria

- [ ] All 5 tool files created
- [ ] Each returns mock data
- [ ] All registered in registry
- [ ] Can invoke each tool via MCP
- [ ] **CRITICAL**: Each file under 100 lines (well below 200-line limit)

## Dependencies
- Completes after: 003-mcp-server/002-tool-registry

## Time Estimate
1 hour

## Testing
- Start MCP server
- Use MCP client to call each tool
- Verify mock responses returned
