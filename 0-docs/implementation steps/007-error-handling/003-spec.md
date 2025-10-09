# Error Handling Module Specification

**Error JSON Format**:
```json
{
  "code": "ErrorCode",
  "message": "Human-readable error message",
  "candidates?": [{"id": "...", "name": "..."}],
  "details?": "Additional context",
  "retryAfter?": 30
}
```

**Error Code Definitions**:

**NotAuthorized**:
- Used when: Missing scopes, invalid token, consent required
- Message: "Authorization failed: insufficient permissions"
- Details: "Required scopes: Tasks.ReadWrite, Group.ReadWrite.All"

**NotFound**:
- Used when: Plan or bucket name not found
- Message: "Plan not found" or "Bucket not found"
- Candidates: Array of available options with id and name/title

**Ambiguous**:
- Used when: Multiple matches for name
- Message: "Multiple plans match" or "Multiple buckets match"
- Candidates: Array of matching options with id and name/title

**RateLimited**:
- Used when: Graph API returns 429
- Message: "Rate limit exceeded"
- RetryAfter: Seconds to wait before retry

**UpstreamError**:
- Used when: Graph API returns other errors
- Message: Sanitized error message from Graph
- Details: Correlation ID for Microsoft support

**ConfigError**:
- Used when: Missing tenant_id or client_id
- Message: "TENANT_ID and CLIENT_ID required in env or config"

**Error Output Pattern** (in CLI commands):
```python
print(json.dumps({"code":"ConfigError","message":"Missing required config"}))
raise typer.Exit(2)
```

**Exception Handling**: Resolution and API errors raise ValueError with JSON string, CLI catches and outputs.
