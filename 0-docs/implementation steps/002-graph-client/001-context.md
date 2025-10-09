# Graph API Client Context

**Purpose**: Provide HTTP client wrapper for Microsoft Graph API calls with error handling.

**Scope**: Handle GET, POST, PATCH requests with authentication, rate limiting, and retries.

**Key Requirements**:
- Bearer token authentication headers
- Automatic retry on 429 (rate limit) responses
- Proper error propagation for CLI error handling
- No token logging in any output
