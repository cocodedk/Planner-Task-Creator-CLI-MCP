# Implementation Plan - Quick Navigation

This directory contains the complete implementation plan for PlannerAgent MVP, broken into the smallest actionable steps.

## 📋 Start Here

### ⚠️ CRITICAL: Every file MUST be under 200 lines. NO EXCEPTIONS.

1. **[000-overview.md](000-overview.md)** - Read this first for execution principles
2. **[architecture-constraints.md](architecture-constraints.md)** - **READ THIS**: File size limit enforcement, modularization, and helper strategy
3. **[mvp-checklist.md](mvp-checklist.md)** - Track overall progress against PRD requirements

## 🗂️ Implementation Workstreams (Execute in Order)

### Phase 1: Setup (Week 1)
**[001-setup/](001-setup/)**
- `001-project-structure.md` - Initialize directories
- `002-extension-dependencies.md` - TypeScript + build tools for extension
- `003-mcp-server-dependencies.md` - Node.js + MCP SDK setup
- `004-shared-types.md` - Common type definitions

**Outcome**: Project scaffold ready for development

---

### Phase 2: Extension Foundation (Week 1-2)
**[002-extension/](002-extension/)**
- `001-manifest-setup.md` - Chrome extension manifest v3
- `002-background-scaffold.md` - Background service worker with message routing
- `003-content-script-scaffold.md` - Content script for Planner pages
- `004-shared-utilities.md` - Logger, retry, validation utilities

**Outcome**: Extension loads and can run on Planner pages

---

### Phase 3: MCP Server Foundation (Week 2)
**[003-mcp-server/](003-mcp-server/)**
- `001-server-scaffold.md` - MCP server startup and protocol
- `002-tool-registry.md` - Tool registration infrastructure
- `003-tool-stubs.md` - Five MVP tools with mock responses

**Outcome**: MCP server running with stub tools

---

### Phase 4: Communication Layer (Week 2-3)
**[004-transport/](004-transport/)**
- `001-transport-interface.md` - Abstract transport interface (SOLID)
- `002-websocket-server.md` - WebSocket server implementation
- `003-websocket-client.md` - Extension WebSocket client with reconnection
- `004-end-to-end-test.md` - Validate complete message flow

**Outcome**: Extension and MCP server can communicate reliably

---

### Phase 5: Read Operations (Week 3)
**[005-read-ops/](005-read-ops/)**
- `001-planner-api-research.md` - Reverse engineer Planner APIs
- `002-api-client-module.md` - HTTP client for Planner
- `003-get-plans-implementation.md` - End-to-end getPlans
- `004-get-tasks-implementation.md` - End-to-end getTasks
- `005-read-ops-polish.md` - Retry logic, error handling, testing

**Outcome**: Can list plans and tasks from Planner

---

### Phase 6: Write Operations (Week 4)
**[006-write-ops/](006-write-ops/)**
- `001-write-api-research.md` - Research create/update endpoints
- `002-create-task-implementation.md` - End-to-end createTask
- `003-update-task-implementation.md` - End-to-end updateTask
- `004-write-ops-polish.md` - Validation, retry, comprehensive testing

**Outcome**: Can create and update tasks in Planner

---

### Phase 7: Delete Operations (Week 4-5)
**[007-delete-ops/](007-delete-ops/)**
- `001-delete-api-research.md` - Research delete endpoint and safety
- `002-confirmation-mechanism.md` - Implement confirmation flow
- `003-delete-implementation.md` - End-to-end deleteTask
- `004-delete-polish.md` - Additional safety, audit trail

**Outcome**: Can safely delete tasks with confirmation

---

### Phase 8: Integration & Release (Week 5-6)
**[008-integration/](008-integration/)**
- `001-end-to-end-scenarios.md` - Complete user workflow testing
- `002-error-scenarios.md` - All error paths tested
- `003-performance-testing.md` - Verify < 3s requirement
- `004-user-documentation.md` - README, SETUP, USAGE, API docs
- `005-final-polish.md` - Code quality, release prep

**Outcome**: MVP ready for production use

---

## 📊 Progress Tracking

Use the **[mvp-checklist.md](mvp-checklist.md)** to track:
- Functional requirements completion
- Non-functional requirements
- Use cases validation
- Architecture constraints adherence
- Documentation completion
- Timeline milestones

## 🎯 Key Metrics

Each document includes:
- **Goal**: What this step achieves
- **Steps**: Detailed actions
- **Acceptance Criteria**: Definition of done
- **Dependencies**: What must complete first
- **Time Estimate**: Planning guidance
- **Notes**: DRY/KISS/YAGNI reminders

## 📏 Architecture Guardrails

All code must follow constraints in **[architecture-constraints.md](architecture-constraints.md)**:
- **200 lines max** per file
- **DRY**: Extract after 2nd use
- **KISS**: Simplest working implementation
- **YAGNI**: No speculative features
- **SOLID**: Single responsibility per module

## 🔄 Workflow

For each workstream:
1. Read all `.md` files in the folder
2. Complete steps in order
3. Check acceptance criteria
4. Mark complete in mvp-checklist.md
5. Move to next folder

## 💡 Tips

- **Exploratory tasks** (API research) may take longer - document findings
- **Testing tasks** are critical - don't skip
- **Polish tasks** ensure quality - take time here
- Update **mvp-checklist.md** regularly to track progress

## 📞 Questions?

- Refer back to **[../prd.md](../prd.md)** for requirements
- Check **[architecture-constraints.md](architecture-constraints.md)** for technical decisions
- Each document is self-contained with context

---

**Total Steps**: 36 atomic implementation tasks
**Total Time**: ~6 weeks for MVP
**Start**: [001-setup/001-project-structure.md](001-setup/001-project-structure.md)
