/**
 * Task Comments Handlers
 * Handlers for reading and adding task comments
 */

import { runCli, parseCliOutput } from "./utils.js";

/**
 * Handle planner_listComments tool
 */
export async function handleListComments(args: {
  task: string;
  plan: string;
}): Promise<any> {
  const cliArgs = ["list-comments-cmd", "--task", args.task, "--plan", args.plan];

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle planner_addComment tool
 */
export async function handleAddComment(args: {
  task: string;
  comment: string;
  plan: string;
}): Promise<any> {
  const cliArgs = [
    "add-comment-cmd",
    "--task",
    args.task,
    "--comment",
    args.comment,
    "--plan",
    args.plan,
  ];

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}
