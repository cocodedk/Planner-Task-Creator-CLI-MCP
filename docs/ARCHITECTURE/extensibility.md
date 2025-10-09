# Extensibility

## Adding New Commands

1. Define command function with `@app.command()` decorator
2. Add parameters with Typer options
3. Implement logic using existing modules
4. Output JSON for machine readability

## Adding New MCP Tools

1. Add tool definition to `TOOLS` array
2. Implement handler in `handleToolCall()`
3. Map MCP arguments to CLI arguments
4. Return parsed JSON output

## Adding New Graph API Endpoints

1. Use existing `get_json()`, `post_json()`, `patch_json()` functions
2. Handle specific endpoint quirks (ETag, pagination, etc.)
3. Add error handling for endpoint-specific errors
