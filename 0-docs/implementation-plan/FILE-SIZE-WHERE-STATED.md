# Where the 200-Line File Size Limit is Stated

This document tracks where the critical 200-line file size limit is mentioned to ensure it's impossible to miss.

## ✅ Top-Level Documents (High Visibility)

### 1. README.md
- **Line 7**: Warning box at the top: "⚠️ CRITICAL: Every file MUST be under 200 lines. NO EXCEPTIONS."
- **Line 10**: Emphasizes architecture-constraints.md as required reading
- **Line 125**: Listed in architecture guardrails section

### 2. 000-overview.md
- **Lines 9-11**: FIRST principle, highlighted section
  ```markdown
  ### ⚠️ CRITICAL: File Size Limit
  **EVERY source file MUST be under 200 logical lines. NO EXCEPTIONS.**
  Split files before reaching this limit. Reject any implementation that exceeds 200 lines.
  ```

### 3. architecture-constraints.md
- **Lines 3-23**: Entire prominent section at the very top
  - Title: "⚠️ CRITICAL FILE SIZE RULE"
  - Subtitle: "ABSOLUTE LIMIT: 200 Lines Per File"
  - Detailed explanation of what counts, why it matters, and enforcement

### 4. FILE-SIZE-ENFORCEMENT.md (NEW)
- **Entire document** (200+ lines) dedicated to enforcement
- Includes:
  - The rule stated clearly
  - Why it exists
  - How to split files
  - Enforcement tools and scripts
  - Common excuses debunked
  - Pre-commit checklist
  - Good vs bad examples

### 5. IMPLEMENTATION_SUMMARY.md
- **Lines 40-52**: Dedicated section highlighting where limit is stated
- **Line 127**: In architecture guardrails list

## ✅ Every Implementation Step (36 Documents)

Each of the 36 implementation step documents now includes the file size limit in one of these ways:

### Explicitly in Acceptance Criteria

**Format 1: Critical reminder**
```markdown
- [ ] **CRITICAL**: All files under 200 lines
```

**Format 2: Warning section**
```markdown
## ⚠️ File Size Reminder
**All source files created must be under 200 lines. NO EXCEPTIONS.**
```

### Documents Updated:

#### 001-setup/ (4 files)
- [x] 001-project-structure.md - Warning section added
- [x] 002-extension-dependencies.md - Warning section added
- [x] 003-mcp-server-dependencies.md - Warning section added
- [x] 004-shared-types.md - Critical checkbox in acceptance criteria

#### 002-extension/ (4 files)
- [x] 001-manifest-setup.md - Warning section added
- [x] 002-background-scaffold.md - Already had checkbox
- [x] 003-content-script-scaffold.md - Already had checkbox
- [x] 004-shared-utilities.md - Already had checkbox

#### 003-mcp-server/ (3 files)
- [x] 001-server-scaffold.md - Already had checkbox
- [x] 002-tool-registry.md - Already had checkbox
- [x] 003-tool-stubs.md - Critical checkbox updated

#### 004-transport/ (4 files)
- [x] 001-transport-interface.md - Critical checkbox updated
- [x] 002-websocket-server.md - Already had checkbox
- [x] 003-websocket-client.md - Already had checkbox
- [x] 004-end-to-end-test.md - Warning section added

#### 005-read-ops/ (5 files)
- [x] 001-planner-api-research.md - Warning section added
- [x] 002-api-client-module.md - Already had checkbox
- [x] 003-get-plans-implementation.md - Critical checkbox added
- [x] 004-get-tasks-implementation.md - Critical checkbox added
- [x] 005-read-ops-polish.md - Critical checkbox added

#### 006-write-ops/ (4 files)
- [x] 001-write-api-research.md - Warning section added
- [x] 002-create-task-implementation.md - Critical checkbox added
- [x] 003-update-task-implementation.md - Critical checkbox added
- [x] 004-write-ops-polish.md - Critical checkbox added

#### 007-delete-ops/ (4 files)
- [x] 001-delete-api-research.md - Warning section added
- [x] 002-confirmation-mechanism.md - Critical checkbox added
- [x] 003-delete-implementation.md - Critical checkbox added
- [x] 004-delete-polish.md - Critical checkbox added

#### 008-integration/ (5 files)
- [x] 001-end-to-end-scenarios.md - Critical checkbox added
- [x] 002-error-scenarios.md - Critical checkbox added
- [x] 003-performance-testing.md - Critical checkbox added
- [x] 004-user-documentation.md - Warning section added
- [x] 005-final-polish.md - Already had checkbox

## ✅ Supporting Documents

### mvp-checklist.md
- **Line 26**: File size in non-functional requirements
- **Line 126**: In architecture constraints checklist

## 📊 Summary Statistics

- **5 top-level documents** explicitly state the 200-line limit
- **1 dedicated enforcement document** (FILE-SIZE-ENFORCEMENT.md)
- **36/36 implementation steps** include file size reminder
- **100% coverage** across all planning documents

## 🎯 Result

**The 200-line file size limit is now IMPOSSIBLE TO MISS.**

Every person reading these documents will encounter the limit:
1. In the first document they read (README)
2. In the first principle (overview)
3. In detailed architecture constraints
4. In a dedicated enforcement guide
5. In every single implementation step they execute

No one can claim they "didn't know" about the limit.
