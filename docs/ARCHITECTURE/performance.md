# Performance Considerations

## Caching

- Token caching reduces authentication overhead
- No caching of plans/buckets (always fetch fresh)
- Config file loaded once per CLI invocation

## Rate Limiting

- Automatic retry on 429 responses
- Respect `Retry-After` header
- Single retry attempt per request

## Optimization

- Minimal dependencies (msal, requests, typer, rich)
- Single-threaded synchronous execution
- Subprocess spawning for MCP server (isolated processes)
