# Bucket Management - Context

## Problem
Current system supports reading buckets (`list-buckets`) but cannot:
- Create new buckets
- Delete buckets
- Rename buckets
- Move all tasks from one bucket to another

This limits workflow automation and forces users to use Planner UI for bucket management.

## Use Cases
1. **Project setup**: Create buckets for sprint phases via CLI/MCP
2. **Workflow evolution**: Rename buckets as project structure changes
3. **Cleanup**: Delete empty/obsolete buckets
4. **Reorganization**: Move all tasks from old bucket to new bucket

## Microsoft Graph API Endpoints

### Create Bucket
```
POST https://graph.microsoft.com/v1.0/planner/buckets
Body: {"name": "Sprint 1", "planId": "abc123", "orderHint": " !"}
Response: Bucket object with id, name, planId
```

### Get Bucket (for ETag)
```
GET https://graph.microsoft.com/v1.0/planner/buckets/{bucketId}
Response: Bucket object with @odata.etag
```

### Update Bucket
```
PATCH https://graph.microsoft.com/v1.0/planner/buckets/{bucketId}
Headers: If-Match: {etag}
Body: {"name": "Sprint 1 - Complete"}
Response: Updated bucket object
```

### Delete Bucket
```
DELETE https://graph.microsoft.com/v1.0/planner/buckets/{bucketId}
Headers: If-Match: {etag}
Response: 204 No Content
```

### List Tasks in Bucket
```
GET https://graph.microsoft.com/v1.0/planner/buckets/{bucketId}/tasks
Response: Array of task objects
```

## Current Limitations
- No bucket creation capability
- No bucket modification capability
- No bucket deletion capability
- Cannot bulk-move tasks between buckets
