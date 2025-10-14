/**
 * Bucket Tool Handlers
 * Handlers for bucket management operations
 */

import { runCli, parseCliOutput } from "./utils.js";

/**
 * Handle planner_createBucket tool
 */
export async function handleCreateBucket(args: {
  name: string;
  plan: string;
}): Promise<any> {
  const result = await runCli([
    "create-bucket",
    "--name", args.name,
    "--plan", args.plan,
  ]);
  return parseCliOutput(result);
}

/**
 * Handle planner_deleteBucket tool
 */
export async function handleDeleteBucket(args: {
  bucket: string;
  plan: string;
}): Promise<any> {
  const result = await runCli([
    "delete-bucket",
    "--bucket", args.bucket,
    "--plan", args.plan,
  ]);
  return parseCliOutput(result);
}

/**
 * Handle planner_renameBucket tool
 */
export async function handleRenameBucket(args: {
  bucket: string;
  newName: string;
  plan: string;
}): Promise<any> {
  const result = await runCli([
    "rename-bucket",
    "--bucket", args.bucket,
    "--new-name", args.newName,
    "--plan", args.plan,
  ]);
  return parseCliOutput(result);
}

/**
 * Handle planner_moveBucketTasks tool
 */
export async function handleMoveBucketTasks(args: {
  source: string;
  target: string;
  plan: string;
}): Promise<any> {
  const result = await runCli([
    "move-bucket-tasks",
    "--source", args.source,
    "--target", args.target,
    "--plan", args.plan,
  ]);
  return parseCliOutput(result);
}
