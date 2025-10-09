#!/usr/bin/env node
/**
 * MCP Server for Microsoft Planner CLI
 * Wraps the Python CLI to expose Planner functionality as MCP tools
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { spawn } from "child_process";
import { homedir } from "os";
import { join } from "path";

/**
 * Get the CLI path from environment or default
 */
function getCliPath(): string {
  return process.env.PLANNER_CLI_PATH || join(homedir(), ".planner-cli", "planner.py");
}

/**
 * Get the Python executable path (prefer venv if available)
 */
function getPythonPath(): string {
  // First, check if PYTHON_PATH is set in environment
  if (process.env.PYTHON_PATH) {
    return process.env.PYTHON_PATH;
  }

  // Check if we're in the project directory with a venv
  const projectDir = process.env.PLANNER_CLI_PATH?.replace("/planner.py", "") || "";
  const venvPython = join(projectDir, "venv", "bin", "python");

  // Check if venv python exists, otherwise use system python3
  try {
    const fs = require("fs");
    if (fs.existsSync(venvPython)) {
      return venvPython;
    }
  } catch {
    // Fall back to system python
  }

  return "python3";
}

/**
 * Run the Python CLI with the given arguments
 */
async function runCli(args: string[]): Promise<{ code: number; stdout: string; stderr: string }> {
  return new Promise((resolve) => {
    const cliPath = getCliPath();
    const pythonPath = getPythonPath();
    const child = spawn(pythonPath, [cliPath, ...args], {
      env: {
        ...process.env,
      },
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    child.on("close", (code) => {
      resolve({ code: code || 0, stdout, stderr });
    });
  });
}

/**
 * Parse CLI output as JSON or return error
 */
function parseCliOutput(result: { code: number; stdout: string; stderr: string }): any {
  if (result.code === 0) {
    try {
      return JSON.parse(result.stdout);
    } catch {
      return { ok: true, message: result.stdout.trim() };
    }
  } else {
    // Try to parse error as JSON
    try {
      return { error: JSON.parse(result.stdout) };
    } catch {
      return { error: { code: "Error", message: result.stderr || result.stdout } };
    }
  }
}

/**
 * Define MCP tools
 */
const TOOLS: Tool[] = [
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
    description: "Create a new task in Microsoft Planner with title, plan, bucket, description, due date, and labels.",
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
];

/**
 * Handle tool execution
 */
async function handleToolCall(name: string, args: any): Promise<any> {
  switch (name) {
    case "planner_initAuth": {
      const result = await runCli(["init-auth"]);
      return parseCliOutput(result);
    }

    case "planner_createTask": {
      const cliArgs = ["add", "--title", args.title];

      if (args.plan) {
        cliArgs.push("--plan", args.plan);
      }
      if (args.bucket) {
        cliArgs.push("--bucket", args.bucket);
      }
      if (args.desc) {
        cliArgs.push("--desc", args.desc);
      }
      if (args.due) {
        cliArgs.push("--due", args.due);
      }
      if (args.labels) {
        cliArgs.push("--labels", args.labels);
      }

      const result = await runCli(cliArgs);
      return parseCliOutput(result);
    }

    case "planner_setDefaults": {
      const result = await runCli([
        "set-defaults",
        "--plan", args.plan,
        "--bucket", args.bucket,
      ]);
      return parseCliOutput(result);
    }

    case "planner_listPlans": {
      const result = await runCli(["list-plans"]);
      return parseCliOutput(result);
    }

    case "planner_listBuckets": {
      const result = await runCli(["list-buckets", "--plan", args.plan]);
      return parseCliOutput(result);
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

/**
 * Main server setup
 */
async function main() {
  const server = new Server(
    {
      name: "planner-mcp-server",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // Handle list_tools request
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools: TOOLS };
  });

  // Handle call_tool request
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      const result = await handleToolCall(name, args || {});

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: errorMessage }, null, 2),
          },
        ],
        isError: true,
      };
    }
  });

  // Start server with stdio transport
  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error("Planner MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
