# 010 - Key Decisions

## D1: Task Resolution
**Choice:** Hybrid (ID or title)
- GUID pattern → use as ID directly
- Otherwise → search by title (case-insensitive)
- Ambiguous → return candidates

## D2: Subtasks = Checklist Items
**Choice:** Use native Planner checklist feature
- Simpler than separate child tasks
- PATCH `/planner/tasks/{id}/details`
- Generate GUID for new items client-side

## D3: ETag Conflicts
**Choice:** Auto-retry once
- Fetch → Update → on 412, retry once
- Covers transient conflicts

## D4: Command Structure
**Choice:** Dedicated commands for common ops
```bash
planner list-tasks --plan X [--bucket Y]
planner complete-task --task "Title"
planner move-task --task "Title" --bucket Y
planner add-subtask --task "Title" --subtask "Sub"
```

## D5: MCP Tool Names
**Choice:** Mirror CLI with camelCase
```
planner_listTasks
planner_completeTask
planner_moveTask
planner_addSubtask
```

## D6: Delete Safety
**Choice:** `--confirm` flag for CLI, direct for MCP
