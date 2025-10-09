# Graph API Client Decisions

**HTTP Library**: Use `requests` for HTTP client (simple, reliable, no external dependencies).

**Authentication**: Authorization Bearer header with access token.

**Rate Limiting**: Handle 429 responses with Retry-After header, sleep and retry once.

**Error Handling**:
- Network errors → raise requests.RequestException
- HTTP error codes → call raise_for_status()
- Preserve correlation IDs from Graph responses for debugging

**Base URL**: `https://graph.microsoft.com/v1.0`

**Security**: Never log Authorization headers or tokens in any output.
