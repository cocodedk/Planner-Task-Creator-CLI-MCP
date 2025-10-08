# Architecture Constraints & Guidelines

## ⚠️ CRITICAL FILE SIZE RULE

### ABSOLUTE LIMIT: 200 Lines Per File

**THIS IS NON-NEGOTIABLE:**
- **Maximum 200 logical lines** per source file
- **NO EXCEPTIONS** - Split files before reaching this limit
- **Split proactively at 150 lines** when complexity grows
- **Reject any pull request** with files exceeding 200 lines
- **Reject files** that become multipurpose or "god" classes

**Why this matters:**
- Enforces Single Responsibility Principle
- Makes code reviewable and maintainable
- Forces proper modularization
- Prevents technical debt accumulation

**What counts as a line:**
- Code statements (not blank lines or comments)
- Import statements count
- Type definitions count

### Modular Structure Pattern

For each major component/module:
```
ModuleName/
├── index.ts           # Barrel exports only
├── types.ts           # All TypeScript interfaces/types
├── utils.ts           # Pure functions, helpers
├── handlers.ts        # Main logic/handlers
├── validation.ts      # Input validation (if needed)
└── constants.ts       # Configuration, literals
```

### Extension-Specific Structure
```
extension/
├── manifest.json
├── background/
│   ├── index.ts       # Entry point
│   ├── messaging.ts   # Message routing
│   └── types.ts       # Message types
├── content/
│   ├── index.ts       # Entry point
│   ├── plannerApi.ts  # Planner API calls
│   ├── domHelpers.ts  # DOM utilities
│   └── types.ts       # Data types
└── shared/
    ├── types.ts       # Shared types
    ├── constants.ts   # URLs, selectors
    └── utils.ts       # Shared helpers
```

### MCP Server Structure
```
mcp-server/
├── index.ts           # Server entry
├── tools/
│   ├── index.ts       # Tool registry
│   ├── getPlans.ts    # Each tool in own file
│   ├── getTasks.ts
│   ├── createTask.ts
│   ├── updateTask.ts
│   └── deleteTask.ts
├── transport/
│   ├── index.ts       # Transport abstraction
│   └── websocket.ts   # WebSocket implementation
├── types.ts           # Server-wide types
└── utils.ts           # Shared utilities
```

## Code Organization Principles

### DRY (Don't Repeat Yourself)
- **Immediate extraction**: When you copy code twice, extract to utility
- **Centralize config**: All URLs, selectors, timeouts in constants
- **Shared types**: Common interfaces in shared types files

### KISS (Keep It Simple)
- **Direct implementations**: No over-abstraction
- **Minimal dependencies**: Only essential packages
- **Clear naming**: Function/variable names reveal intent

### YAGNI (You Aren't Gonna Need It)
- **No speculative code**: Only implement current requirements
- **No premature optimization**: Profile before optimizing
- **No unused features**: Remove commented code immediately

### SOLID Application

**Single Responsibility**
- Each file handles ONE concern
- `plannerApi.ts` → API calls only
- `validation.ts` → Input validation only
- `types.ts` → Type definitions only

**Open/Closed**
- Extend via composition, not modification
- Add new tools by creating new files, not editing registry

**Interface Segregation**
- Narrow interfaces (e.g., `ReadOnlyPlannerAPI` vs `FullPlannerAPI`)
- Each consumer depends only on what it needs

**Dependency Inversion**
- Depend on interfaces, not concrete implementations
- Inject transport layer, don't hardcode WebSocket

## Helper Strategy

### When to Create Helpers

**Create utility when:**
- Logic is used 2+ times
- Function is pure (no side effects)
- Logic is testable in isolation
- Function has clear single purpose

**Don't create helper for:**
- One-off operations
- Tightly coupled business logic
- Simple one-liners (use inline)

### Helper Organization

```typescript
// ❌ BAD: Monolithic helpers
helpers/
└── utils.ts  // 500 lines of mixed utilities

// ✅ GOOD: Focused helpers
helpers/
├── dateUtils.ts      // Date formatting/parsing
├── validation.ts     // Input validation
├── stringUtils.ts    // String manipulation
└── retry.ts          // Retry logic
```

### Helper Naming Convention

- `[domain][Action]` pattern: `parseTaskDate`, `validatePlanId`
- Verb-based for actions: `formatDate`, `retryWithBackoff`
- Noun-based for getters: `taskTitle`, `planName`

## Error Handling Strategy

### Error Types
```typescript
// types.ts
interface OperationError {
  code: string;           // ERROR_TASK_NOT_FOUND
  message: string;        // Human-readable
  context?: unknown;      // Additional data
  retryable: boolean;     // Can retry?
}
```

### Error Propagation
- Content script → catches, wraps → background
- Background → catches, wraps → MCP server
- MCP server → formats → AI agent

### No Silent Failures
- Every error logged with context
- Every error returned with actionable message
- No generic "something went wrong"

## Testing Strategy (For MVP)

### Manual Testing Priority
- Extension → Planner UI integration
- Each MCP tool end-to-end
- Error scenarios (invalid IDs, network failures)

### Automated Testing (Nice-to-Have)
- Unit tests for pure utilities
- Integration tests for MCP tools
- E2E tests deferred post-MVP

## Performance Targets

- Operation completion: < 3 seconds
- Extension memory: < 50MB
- MCP server startup: < 1 second
- No UI blocking operations

## Security Constraints

- Use existing browser session (no credential storage)
- No external API calls (all through browser context)
- Minimal permissions in manifest
- No sensitive data in logs
