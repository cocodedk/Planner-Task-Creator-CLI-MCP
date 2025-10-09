/**
 * MCP Tools Definitions
 * Defines all available MCP tools for the Planner server
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

export const TOOLS: Tool[] = [
  {
    name: "planner_initAuth",
    description: "Initialize authentication with Microsoft. Returns verification URL and code for device flow.",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "planner_createTask",
    description: "Create a new task in Microsoft Planner with title, plan, bucket, description, due date, labels, and assignee.",
    inputSchema: {
      type: "object",
      properties: {
        title: {
          type: "string",
          description: "Task title (required)",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (optional if default is set)",
        },
        bucket: {
          type: "string",
          description: "Bucket name or ID (optional if default is set)",
        },
        desc: {
          type: "string",
          description: "Task description (optional)",
        },
        due: {
          type: "string",
          description: "Due date in YYYY-MM-DD format (optional)",
        },
        labels: {
          type: "string",
          description: "Comma-separated labels like 'Label1,Label3' (optional)",
        },
        assignee: {
          type: "string",
          description: "Comma-separated user emails or User IDs (e.g., user1@example.com,user2@example.com) (optional)",
        },
      },
      required: ["title"],
    },
  },
  {
    name: "planner_setDefaults",
    description: "Set default plan and bucket for task creation.",
    inputSchema: {
      type: "object",
      properties: {
        plan: {
          type: "string",
          description: "Default plan name or ID",
        },
        bucket: {
          type: "string",
          description: "Default bucket name or ID",
        },
      },
      required: ["plan", "bucket"],
    },
  },
  {
    name: "planner_listPlans",
    description: "List all available plans accessible to the user.",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "planner_listBuckets",
    description: "List all buckets in a specific plan.",
    inputSchema: {
      type: "object",
      properties: {
        plan: {
          type: "string",
          description: "Plan name or ID",
        },
      },
      required: ["plan"],
    },
  },
  {
    name: "planner_listTasks",
    description: "List tasks in a plan or bucket. Can filter to show only incomplete tasks.",
    inputSchema: {
      type: "object",
      properties: {
        plan: {
          type: "string",
          description: "Plan name or ID (required)",
        },
        bucket: {
          type: "string",
          description: "Bucket name or ID (optional)",
        },
        incompleteOnly: {
          type: "boolean",
          description: "Show only incomplete tasks (optional, default: false)",
        },
      },
      required: ["plan"],
    },
  },
  {
    name: "planner_findTask",
    description: "Find a task by ID or title. Returns full task details.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID (GUID) or task title",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for title-based search)",
        },
      },
      required: ["task"],
    },
  },
  {
    name: "planner_completeTask",
    description: "Mark a task as complete (sets percentComplete to 100).",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID or title",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for title-based search)",
        },
      },
      required: ["task"],
    },
  },
  {
    name: "planner_moveTask",
    description: "Move a task to a different bucket within the same plan.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID or title",
        },
        bucket: {
          type: "string",
          description: "Target bucket name or ID",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for resolution)",
        },
      },
      required: ["task", "bucket"],
    },
  },
  {
    name: "planner_addSubtask",
    description: "Add a subtask (checklist item) to a task.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID or title",
        },
        subtask: {
          type: "string",
          description: "Subtask title",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for title-based search)",
        },
      },
      required: ["task", "subtask"],
    },
  },
  {
    name: "planner_listSubtasks",
    description: "List all subtasks (checklist items) for a task.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID or title",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for title-based search)",
        },
      },
      required: ["task"],
    },
  },
  {
    name: "planner_completeSubtask",
    description: "Mark a subtask (checklist item) as complete.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID or title",
        },
        subtask: {
          type: "string",
          description: "Subtask title to complete",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for title-based search)",
        },
      },
      required: ["task", "subtask"],
    },
  },
  {
    name: "planner_deleteTask",
    description: "Delete a task. No confirmation required for MCP (unlike CLI).",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID or title",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for title-based search)",
        },
      },
      required: ["task"],
    },
  },
  {
    name: "planner_updateTask",
    description: "Update labels on an existing task.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Task ID or title (required)",
        },
        plan: {
          type: "string",
          description: "Plan name or ID (required for title-based search)",
        },
        labels: {
          type: "string",
          description: "Comma-separated labels like 'Label1,Label3' (optional, empty string to clear all labels)",
        },
      },
      required: ["task"],
    },
  },
];
