/**
 * Tool Handlers - Main Router
 * Routes tool calls to appropriate handler functions
 */

import {
  handleInitAuth,
  handleSetDefaults,
  handleListPlans,
  handleListBuckets,
  handleCreateTask,
} from "./handlers-core.js";

import {
  handleListTasks,
  handleFindTask,
  handleCompleteTask,
  handleMoveTask,
  handleDeleteTask,
  handleUpdateTask,
} from "./handlers-tasks.js";

import {
  handleAddSubtask,
  handleListSubtasks,
  handleCompleteSubtask,
} from "./handlers-subtasks.js";

import {
  handleSearchUsers,
  handleLookupUser,
} from "./handlers-users.js";

import {
  handleCreateBucket,
  handleDeleteBucket,
  handleRenameBucket,
  handleMoveBucketTasks,
} from "./handlers-buckets.js";

import {
  handleListComments,
  handleAddComment,
} from "./handlers-comments.js";

/**
 * Handle tool execution by routing to specific handlers
 */
export async function handleToolCall(name: string, args: any): Promise<any> {
  switch (name) {
    // Core tools
    case "planner_initAuth":
      return handleInitAuth();

    case "planner_setDefaults":
      return handleSetDefaults(args);

    case "planner_listPlans":
      return handleListPlans();

    case "planner_listBuckets":
      return handleListBuckets(args);

    case "planner_createTask":
      return handleCreateTask(args);

    // Task management tools
    case "planner_listTasks":
      return handleListTasks(args);

    case "planner_findTask":
      return handleFindTask(args);

    case "planner_completeTask":
      return handleCompleteTask(args);

    case "planner_moveTask":
      return handleMoveTask(args);

    case "planner_deleteTask":
      return handleDeleteTask(args);

    case "planner_updateTask":
      return handleUpdateTask(args);

    // Subtask tools
    case "planner_addSubtask":
      return handleAddSubtask(args);

    case "planner_listSubtasks":
      return handleListSubtasks(args);

    case "planner_completeSubtask":
      return handleCompleteSubtask(args);

    // User tools
    case "planner_searchUsers":
      return handleSearchUsers(args);

    case "planner_lookupUser":
      return handleLookupUser(args);

    // Bucket management tools
    case "planner_createBucket":
      return handleCreateBucket(args);

    case "planner_deleteBucket":
      return handleDeleteBucket(args);

    case "planner_renameBucket":
      return handleRenameBucket(args);

    case "planner_moveBucketTasks":
      return handleMoveBucketTasks(args);

    // Comment tools
    case "planner_listComments":
      return handleListComments(args);

    case "planner_addComment":
      return handleAddComment(args);

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
