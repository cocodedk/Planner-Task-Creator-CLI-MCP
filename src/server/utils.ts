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
      resolve({ code: code || 0, stdout, stderr });
    });
  });
}

/**
 * Parse CLI output as JSON or return error
 */
export function parseCliOutput(result: { code: number; stdout: string; stderr: string }): any {
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
