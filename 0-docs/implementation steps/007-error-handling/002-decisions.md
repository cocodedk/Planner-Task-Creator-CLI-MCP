# Error Handling Module Decisions

**Error Format**: JSON with `code`, `message`, and optional `candidates` or `details` fields.

**Error Codes**:
- `NotAuthorized`: Missing permissions or scopes
- `NotFound`: Resource not found (plan, bucket)
- `Ambiguous`: Multiple matches found
- `RateLimited`: API rate limit exceeded
- `UpstreamError`: Graph API errors
- `ConfigError`: Missing required configuration

**Response Strategy**: All errors output as JSON to stdout for machine consumption.

**Exit Strategy**: Use `typer.Exit(2)` for configuration errors, raise exceptions for others.

**Error Context**: Include helpful details like candidate lists, required scopes, retry timing.
