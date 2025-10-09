# Authentication Module Specification

**Function**: `get_tokens(tenant_id: str, client_id: str) -> str`

**Parameters**:
- `tenant_id`: Azure AD tenant ID (required)
- `client_id`: Azure AD app registration client ID (required)

**Returns**: Valid access token string

**Implementation Steps**:
1. Create MSAL PublicClientApplication with authority URL
2. Initialize SerializableTokenCache
3. Load existing cache from `~/.planner-cli/msal_cache.bin` if exists
4. Try silent token acquisition from cache
5. If no cached token, initiate device code flow
6. Display verification URL and user code to user
7. Poll for token via device flow
8. Save updated cache to filesystem
9. Set cache file permissions to 0600
10. Return access token

**Cache Path**: `~/.planner-cli/msal_cache.bin`

**Error Cases**:
- Missing tenant_id or client_id → RuntimeError
- Device flow initiation failure → RuntimeError
- Token acquisition failure → RuntimeError with error_description
