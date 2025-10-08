# 002-extension/004: Shared Extension Utilities

## Goal
Create focused utility modules for common operations used across extension.

## Steps

1. **Create shared utilities structure**
   ```
   extension/src/shared/
   ├── logger.ts          # Structured logging
   ├── retry.ts           # Retry logic with exponential backoff
   ├── validation.ts      # Input validation helpers
   └── constants.ts       # Extension-wide constants
   ```

2. **Implement logger.ts** (<100 lines)
   ```typescript
   - log(level, message, context)
   - debug(), info(), warn(), error() helpers
   - Prefix with timestamp and component name
   - Conditional logging based on environment
   ```

3. **Implement retry.ts** (<100 lines)
   ```typescript
   - retryWithBackoff(fn, options)
   - Exponential backoff calculation
   - Max retries configuration
   - Error predicate (should retry?)
   ```

4. **Implement validation.ts** (<100 lines)
   ```typescript
   - validatePlanId(id)
   - validateTaskId(id)
   - validateDateString(date)
   - Each returns ValidationResult
   ```

5. **Implement constants.ts** (<50 lines)
   ```typescript
   - PLANNER_BASE_URL
   - MESSAGE_TIMEOUT
   - MAX_RETRIES
   - API endpoint patterns
   ```

## Acceptance Criteria

- [ ] All utility files created
- [ ] Each file under 200 lines (aim for under 100)
- [ ] Pure functions, no side effects (except logger)
- [ ] Each utility has single, clear purpose
- [ ] Can be imported and used in background/content

## Dependencies
- Completes after: 002-extension/002-background-scaffold

## Time Estimate
1 hour

## DRY Principle Application
- Extract ANY repeated logic here immediately
- If you copy-paste twice, extract to utility
- Update existing code to use these utilities
