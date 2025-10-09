# MCP Server Usage

## In Claude Desktop

**Example 1: Simple Task Creation**
```
User: Can you create a task in my Planner called "Review Q4 metrics"?

Claude: I'll create that task for you.
[Uses planner_createTask tool]

Task created successfully:
- Task ID: abc123...
- Title: Review Q4 metrics
- URL: https://planner.cloud.microsoft/...
```

**Example 2: Task with Details**
```
User: Create a task titled "Prepare presentation" with a description
"Slides for quarterly review" and due date December 31st, 2024.

Claude: I'll create that task with all the details.
[Uses planner_createTask with desc and due parameters]

Task created:
- Title: Prepare presentation
- Description: Slides for quarterly review
- Due: 2024-12-31
```

**Example 3: List Plans First**
```
User: What plans do I have available?

Claude: Let me check your available plans.
[Uses planner_listPlans tool]

You have 3 plans:
1. Work Projects (Engineering Team)
2. Personal Tasks (My Personal Group)
3. Q4 2024 (Management)
```

**Example 4: Set Defaults**
```
User: Set my default plan to "Work Projects" and bucket to "This Week"

Claude: I'll update your defaults.
[Uses planner_setDefaults tool]

Defaults updated successfully.
```

## Using MCP Server Directly

If you're building your own MCP client:

```typescript
// Example MCP client code
const result = await client.callTool("planner_createTask", {
  title: "Implement new feature",
  plan: "Web Development",
  bucket: "Sprint 12",
  desc: "Add user profile customization",
  due: "2024-12-31",
  labels: "Label1,Label2"
});

console.log(result);
```
