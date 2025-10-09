/**
 * User-related Tool Handlers
 * Handles user search and lookup operations
 */

import { runCli, parseCliOutput } from "./utils.js";

/**
 * Handle user search by display name
 */
export async function handleSearchUsers(args: { query: string }): Promise<any> {
  const cliArgs = ["user", "search", args.query];

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}

/**
 * Handle user lookup/resolution
 */
export async function handleLookupUser(args: {
  user: string;
  noSearch?: boolean;
}): Promise<any> {
  const cliArgs = ["user", "lookup", args.user];

  if (args.noSearch) {
    cliArgs.push("--no-search");
  }

  const result = await runCli(cliArgs);
  return parseCliOutput(result);
}
