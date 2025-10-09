# Project Roadmap

## v1.0 - Task Creation ✅ (Complete)
**Status**: Shipped
**Capabilities**:
- Device code authentication
- Create tasks with description, due date, labels
- Plan/bucket resolution (name → ID)
- Default plan/bucket configuration
- MCP server integration

**CLI Commands**:
- `planner init-auth`
- `planner add`
- `planner set-defaults`
- `planner list-plans`
- `planner list-buckets`

**MCP Tools**: 5 tools

---

## v2.0 - Task Management 🔄 (Planned)
**Status**: Design complete, ready for implementation
**Capabilities**:
- List/find existing tasks
- Mark tasks complete
- Move tasks between buckets
- Split tasks into subtasks (checklist)
- Delete tasks

**New CLI Commands**:
- `planner list-tasks`
- `planner find-task`
- `planner complete-task`
- `planner move-task`
- `planner add-subtask`
- `planner list-subtasks`
- `planner complete-subtask`
- `planner delete-task`

**New MCP Tools**: +8 tools (total 13)

**Effort**: 8-12 hours across 4 phases

**Docs**: `0-docs/implementation steps/010-task-management/`
- 11 spec files (all <80 lines)
- Phase-by-phase implementation plan
- Ready to execute

---

## v3.0 - Advanced Features (Future)
**Status**: Not scoped yet
**Potential features**:
- Task assignments with user resolution
- Priority management
- Task comments
- Attachments
- Recurring tasks
- Bulk operations
- Advanced filters
