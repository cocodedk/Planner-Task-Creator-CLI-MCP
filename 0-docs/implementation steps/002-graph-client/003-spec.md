# Graph API Client Specification

**Functions**:
- `auth_headers(token: str) -> dict`
- `get_json(url: str, token: str) -> dict`
- `post_json(url: str, token: str, payload: dict) -> dict`
- `patch_json(url: str, token: str, payload: dict, etag: str) -> dict`

**auth_headers Implementation**:
- Return `{"Authorization": f"Bearer {token}", "Content-Type": "application/json"}`

**get_json Implementation**:
1. Make GET request with auth headers
2. Check for 429 status code
3. If 429, extract Retry-After header (default 2 seconds), sleep, retry once
4. Call raise_for_status() on response
5. Return response.json()

**post_json Implementation**:
1. Make POST request with auth headers and JSON payload
2. Check for 429 status code
3. If 429, extract Retry-After header (default 2 seconds), sleep, retry once
4. Call raise_for_status() on response
5. Return response.json()

**patch_json Implementation**:
1. Add If-Match header to auth headers
2. Make PATCH request with auth headers, JSON payload, and etag
3. Call raise_for_status() on response
4. Return response.json() if response has content, else return empty dict

**Error Handling**: All functions raise requests.RequestException on network/HTTP errors.
