/**
 * Subtask Handlers
 * Handlers for subtask/checklist operations
 */

import { runCli, parseCliOutput } from "./utils.js";

/**
 * Handle planner_addSubtask tool
 */
export async function handleAddSubtask(args: {
  task: string;
  subtask: string;
  plan?: string;
}): Promise<any> {
  const cliArgs = ["add-subtask-cmd", "--task", args.task, "--subtask", args.subtask];

  if (args.plan) {
    cliArgs.push("--plan", args.plan);
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle planner_listSubtasks tool
 */
export async function handleListSubtasks(args: { task: string; plan?: string }): Promise<any> {
  const cliArgs = ["list-subtasks-cmd", "--task", args.task];

  if (args.plan) {
    cliArgs.push("--plan", args.plan);
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle planner_completeSubtask tool
 */
export async function handleCompleteSubtask(args: {
  task: string;
  subtask: string;
  plan?: string;
}): Promise<any> {
  const cliArgs = ["complete-subtask-cmd", "--task", args.task, "--subtask", args.subtask];

  if (args.plan) {
    cliArgs.push("--plan", args.plan);
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}
