/**
 * Task Management Handlers
 * Handlers for task operations (list, find, complete, move, delete)
 */

import { runCli, parseCliOutput } from "./utils.js";

/**
 * Handle planner_listTasks tool
 */
export async function handleListTasks(args: {
  plan: string;
  bucket?: string;
  incompleteOnly?: boolean;
}): Promise<any> {
  const cliArgs = ["list-tasks-cmd", "--plan", args.plan];

  if (args.bucket) {
    cliArgs.push("--bucket", args.bucket);
  }
  if (args.incompleteOnly) {
    cliArgs.push("--incomplete");
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle planner_findTask tool
 */
export async function handleFindTask(args: { task: string; plan?: string }): Promise<any> {
  const cliArgs = ["find-task-cmd", "--task", args.task];

  if (args.plan) {
    cliArgs.push("--plan", args.plan);
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle planner_completeTask tool
 */
export async function handleCompleteTask(args: { task: string; plan?: string }): Promise<any> {
  const cliArgs = ["complete-task-cmd", "--task", args.task];

  if (args.plan) {
    cliArgs.push("--plan", args.plan);
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle planner_moveTask tool
 */
export async function handleMoveTask(args: {
  task: string;
  bucket: string;
  plan?: string;
}): Promise<any> {
  const cliArgs = ["move-task-cmd", "--task", args.task, "--bucket", args.bucket];

  if (args.plan) {
    cliArgs.push("--plan", args.plan);
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle planner_deleteTask tool
 */
export async function handleDeleteTask(args: { task: string; plan?: string }): Promise<any> {
  const cliArgs = ["delete-task-cmd", "--task", args.task, "--confirm"];

  if (args.plan) {
    cliArgs.push("--plan", args.plan);
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}
