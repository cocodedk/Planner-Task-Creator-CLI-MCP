/**
 * Core Tool Handlers
 * Handlers for authentication and configuration tools
 */

import { runCli, parseCliOutput } from "./utils.js";

/**
 * Handle planner_initAuth tool
 */
export async function handleInitAuth(): Promise<any> {
  const result = await runCli(["init-auth"]);
  return parseCliOutput(result);
}

/**
 * Handle planner_setDefaults tool
 */
export async function handleSetDefaults(args: { plan: string; bucket: string }): Promise<any> {
  const result = await runCli([
    "set-defaults",
    "--plan", args.plan,
    "--bucket", args.bucket,
  ]);
  return parseCliOutput(result);
}

/**
 * Handle planner_listPlans tool
 */
export async function handleListPlans(): Promise<any> {
  const result = await runCli(["list-plans"]);
  return parseCliOutput(result);
}

/**
 * Handle planner_listBuckets tool
 */
export async function handleListBuckets(args: { plan: string }): Promise<any> {
  const result = await runCli(["list-buckets", "--plan", args.plan]);
  return parseCliOutput(result);
}

/**
 * Handle planner_createTask tool
 */
export async function handleCreateTask(args: {
  title: string;
  plan?: string;
  bucket?: string;
  desc?: string;
  due?: string;
  labels?: string;
}): Promise<any> {
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
