/**
 * Utility Functions
 * Helper functions for path resolution and CLI execution
 */

import { spawn } from "child_process";
import { homedir } from "os";
import { join } from "path";
import { existsSync } from "fs";

/**
 * Get the CLI path from environment or default
 */
export function getCliPath(): string {
  return process.env.PLANNER_CLI_PATH || join(homedir(), ".planner-cli", "planner.py");
}

/**
 * Get the Python executable path (prefer venv if available)
 */
export function getPythonPath(): string {
  // First, check if PYTHON_PATH is set in environment
  if (process.env.PYTHON_PATH) {
    return process.env.PYTHON_PATH;
  }

  // Check if we're in the project directory with a venv
  const projectDir = process.env.PLANNER_CLI_PATH?.replace("/planner.py", "") || "";
  const venvPython = join(projectDir, "venv", "bin", "python");

  // Check if venv python exists, otherwise use system python3
  try {
    if (existsSync(venvPython)) {
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
export async function runCli(args: string[]): Promise<{ code: number; stdout: string; stderr: string }> {
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
      // Debug logging for troubleshooting
      if (code !== 0) {
        console.error(`[MCP Debug] CLI failed with code ${code}`);
        console.error(`[MCP Debug] stdout: ${stdout.substring(0, 200)}`);
        console.error(`[MCP Debug] stderr: ${stderr.substring(0, 200)}`);
      }
      resolve({ code: code || 0, stdout, stderr });
    });
  });
}

/**
 * Parse CLI output as JSON or throw error
 */
export function parseCliOutput(result: { code: number; stdout: string; stderr: string }): any {
  if (result.code === 0) {
    try {
      return JSON.parse(result.stdout.trim());
    } catch {
      return { ok: true, message: result.stdout.trim() };
    }
  } else {
    // Try to parse error as JSON from stdout first, then stderr
    let errorObj: any;
    const stdoutTrimmed = result.stdout.trim();
    const stderrTrimmed = result.stderr.trim();

    // Try parsing stdout as JSON
    try {
      if (stdoutTrimmed) {
        errorObj = JSON.parse(stdoutTrimmed);
      } else {
        throw new Error("Empty stdout");
      }
    } catch {
      // Try parsing stderr as JSON
      try {
        if (stderrTrimmed) {
          errorObj = JSON.parse(stderrTrimmed);
        } else {
          throw new Error("Empty stderr");
        }
      } catch {
        // Neither is valid JSON, create error object from available info
        const errorMessage = stderrTrimmed || stdoutTrimmed || "Unknown error";
        errorObj = { code: "Error", message: errorMessage };
      }
    }

    // Throw error so MCP server can properly mark it as an error
    // Extract error message from various possible formats
    const errorMessage =
      errorObj.message ||
      errorObj.error?.message ||
      (typeof errorObj === 'string' ? errorObj : JSON.stringify(errorObj));
    const error = new Error(errorMessage);
    (error as any).errorData = errorObj;
    throw error;
  }
}
