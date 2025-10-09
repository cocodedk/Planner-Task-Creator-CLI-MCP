# Authentication Module Context

**Purpose**: Implement secure OAuth authentication for Microsoft Graph API using device code flow.

**Scope**: Handle MSAL token acquisition, caching, and renewal for headless CLI usage.

**Key Requirements**:
- Device code flow for terminal authentication
- Secure token caching to filesystem
- Automatic token renewal via refresh tokens
- No tokens stored in config files or logs
