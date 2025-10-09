# Testing Architecture

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── test_auth.py          # Authentication tests
├── test_config.py        # Configuration tests
├── test_resolution.py    # Resolution tests
├── test_task_creation.py # Task creation tests
└── test_cli_commands.py  # CLI integration tests
```

## Mock Strategy

- **MSAL**: Mock `PublicClientApplication` and `SerializableTokenCache`
- **Requests**: Mock `requests.get/post/patch` for Graph API calls
- **File System**: Use `tmp_path` fixtures for config and cache files

## Test Coverage

- Unit tests for individual functions
- Integration tests for CLI commands
- Mock external dependencies (MSAL, Graph API)
- Test all error paths and edge cases
