# Resolution Module Decisions

**ID Detection**: GUID format validation using pattern matching (32 hex digits with hyphens).

**Matching Strategy**: Case-insensitive comparison of name fields.

**API Endpoints**:
- Plans: `GET /me/planner/plans` (augment with group displayName)
- Buckets: `GET /planner/plans/{planId}/buckets`

**Error Types**:
- **NotFound**: No matches found, return all candidates
- **Ambiguous**: Multiple matches, return all candidates with IDs
- **UpstreamError**: Graph API errors, preserve correlation ID

**Response Format**: JSON error objects with `code`, `message`, and `candidates` array.

**Caching**: No caching - always fetch fresh data for accuracy.
