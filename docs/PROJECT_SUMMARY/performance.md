# Performance Characteristics

- **Startup time**: < 1 second (with cached token)
- **Task creation**: 1-2 seconds (includes resolution + API calls)
- **Memory footprint**: ~50MB Python process
- **Dependencies**: Minimal, only essential packages
- **Caching**: Token cache reduces auth overhead

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
