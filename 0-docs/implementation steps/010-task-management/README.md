# 010 - Task Management Operations

## Summary
Extends CLI and MCP with full task lifecycle management.

## Documentation Files
- `001-context.md` - Problem, scope, phases
- `002-decisions.md` - Key architectural choices

## Implementation Order

### Phase 1: Read Operations
1. `010-1-list-tasks.md` - List tasks by plan/bucket
2. `010-2-find-task.md` - Resolve task by ID or title

### Phase 2: Update Operations
3. `010-3-complete-task.md` - Mark task complete
4. `010-4-move-task.md` - Move to different bucket

### Phase 3: Subtasks (Checklist)
5. `010-5-add-subtask.md` - Add checklist item
6. `010-6-list-subtasks.md` - List checklist items
7. `010-7-complete-subtask.md` - Mark checklist item complete

### Phase 4: Delete
8. `010-8-delete-task.md` - Delete task with safety

## New CLI Commands
```bash
planner list-tasks --plan X [--bucket Y] [--incomplete]
planner complete-task --task "Title"
planner move-task --task "Title" --bucket "Bucket"
planner add-subtask --task "Title" --subtask "Sub"
planner list-subtasks --task "Title"
planner complete-subtask --task "Title" --subtask "Sub"
planner delete-task --task "Title" --confirm
```

## New MCP Tools
- `planner_listTasks`
- `planner_findTask`
- `planner_completeTask`
- `planner_moveTask`
- `planner_addSubtask`
- `planner_listSubtasks`
- `planner_completeSubtask`
- `planner_deleteTask`

## Answer to Original Questions
✅ **Find task and split into subtasks**: Yes (find + add-subtask)
✅ **Mark task as done**: Yes (complete-task)
✅ **Move task to different bucket**: Yes (move-task)
