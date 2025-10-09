# Security Considerations

## Token Security

- Tokens stored in `~/.planner-cli/msal_cache.bin` with 0600 permissions
- Tokens never logged or included in output
- Automatic token refresh via refresh tokens
- Cache encrypted by MSAL library

## Configuration Security

- Config file has 0600 permissions (owner only)
- Sensitive values (tenant_id, client_id) treated as confidential
- No hardcoded credentials in source code

## API Security

- OAuth 2.0 device code flow (no client secrets required)
- Required scopes explicitly declared
- Bearer token authentication for all API calls
- HTTPS for all Graph API communication
