# ⚠️ FILE SIZE LIMIT ENFORCEMENT

## THE RULE

### **EVERY SOURCE FILE MUST BE UNDER 200 LOGICAL LINES**

This is **NON-NEGOTIABLE**. No exceptions. No excuses.

## What This Means

### What Counts as a Line
- **Counts**: Code statements, import statements, type definitions
- **Doesn't count**: Blank lines, pure comment lines
- **Use**: Line count from your editor, or `grep -vc "^\s*$" filename.ts`

### The Limits
- **Hard limit**: 200 lines
- **Warning threshold**: 150 lines (start planning to split)
- **Good target**: 100-150 lines per file

## Why This Rule Exists

1. **Forces Single Responsibility**: If a file is getting large, it's doing too much
2. **Improves Maintainability**: Smaller files are easier to understand and modify
3. **Enables Review**: Reviewable changes stay focused
4. **Prevents Technical Debt**: No "god files" that become unmaintainable
5. **Enforces Architecture**: Can't ignore modularization when forced to split

## How to Split Files

### When a file approaches 150 lines:

**For Components/Modules:**
```
MyFeature/
├── index.ts        # Exports only
├── types.ts        # Type definitions
├── utils.ts        # Pure utilities
├── handlers.ts     # Main logic
└── validation.ts   # Input validation
```

**For API Modules:**
```
api/
├── index.ts        # Exports
├── client.ts       # HTTP client
├── endpoints.ts    # URL builders
├── parsers.ts      # Response parsing
└── types.ts        # Types
```

**For Tools (MCP Server):**
```
tools/
├── index.ts        # Registry
├── getPlans.ts     # One tool
├── getTasks.ts     # One tool
├── createTask.ts   # One tool
└── ...            # One file per tool
```

## Enforcement Checklist

### During Implementation
- [ ] Check line count before committing any file
- [ ] Split files that exceed 150 lines
- [ ] Never commit files over 200 lines

### During Code Review
- [ ] Reject PRs with files over 200 lines
- [ ] Request splitting for files over 150 lines
- [ ] Verify logical cohesion in each file

### Tools
```bash
# Count lines in a file (excluding blanks)
grep -vc "^\s*$" yourfile.ts

# Find all files over 200 lines
find . -name "*.ts" -exec sh -c 'lines=$(grep -vc "^\s*$" "$1"); if [ $lines -gt 200 ]; then echo "$1: $lines lines"; fi' _ {} \;

# Find all files over 150 lines (warning)
find . -name "*.ts" -exec sh -c 'lines=$(grep -vc "^\s*$" "$1"); if [ $lines -gt 150 ]; then echo "⚠️ $1: $lines lines"; fi' _ {} \;
```

## Common Excuses (and Why They Don't Work)

❌ **"But this component needs all these methods"**
→ Extract methods to utility modules

❌ **"But these are all related types"**
→ Split into domain-specific type files

❌ **"But the API response is complex"**
→ Split parsing into multiple focused parsers

❌ **"But it's mostly imports"**
→ Too many imports means too many dependencies, refactor

❌ **"But we're almost done with this feature"**
→ Technical debt starts here, split now

❌ **"But splitting will make it harder to understand"**
→ Opposite is true: focused files are easier to understand

## What Success Looks Like

### Good File Example (120 lines)
```typescript
// tools/getTasks.ts
import { Tool, ToolResult } from './types';
import { sendMessage } from '../transport';
import { validatePlanId } from '../validation';
import { logger } from '../logger';

// Clear, focused purpose
export const getTasks: Tool = async (input) => {
  // Validation
  const validation = validatePlanId(input.planId);
  if (!validation.valid) {
    return { error: validation.error };
  }

  // Business logic
  try {
    const result = await sendMessage({
      type: 'GET_TASKS',
      payload: { planId: input.planId }
    });
    return { data: result };
  } catch (error) {
    logger.error('getTasks failed', { error, planId: input.planId });
    return { error: 'Failed to retrieve tasks' };
  }
};
```

**Why this works:**
- Single responsibility (get tasks)
- Dependencies imported, not implemented here
- Validation logic in separate module
- Under 50 lines, room to grow

### Bad File Example (400 lines) ❌
```typescript
// api.ts
// Everything in one file:
// - All endpoints
// - All parsers
// - All validation
// - All error handling
// - All types
// ... 400 lines later

// THIS MUST BE SPLIT!
```

## Pre-Commit Checklist

Before committing ANY file:
1. Count lines: `grep -vc "^\s*$" yourfile.ts`
2. If > 200: **STOP, SPLIT IMMEDIATELY**
3. If > 150: **Plan to split soon**
4. If < 150: Proceed with commit

## Remember

**The 200-line limit is not a suggestion. It's an architectural constraint that protects code quality.**

If you can't fit your logic in 200 lines, you're not extracting enough.
Split early, split often.
