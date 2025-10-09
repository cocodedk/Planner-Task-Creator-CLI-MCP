# Authentication Module Decisions

**Technology Choice**: Use `msal` Python library for OAuth implementation.

**Flow Selection**: Device code flow - suitable for CLI/headless environments.

**Caching Strategy**: MSAL SerializableTokenCache to filesystem with 0600 permissions.

**Security Model**:
- Tokens never logged or stored in config files
- Cache file permissions set to 0600 (owner read/write only)
- Authority URL constructed from tenant_id
- Required scopes: Tasks.ReadWrite, Group.ReadWrite.All, offline_access

**Error Handling**: Let MSAL handle auth errors; wrap in RuntimeError for CLI.
