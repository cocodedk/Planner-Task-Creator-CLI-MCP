# Testing Module Specification

**Test Files**:
- `test_auth.py`: Authentication module tests
- `test_config.py`: Configuration management tests
- `test_resolution.py`: Plan/bucket resolution tests
- `test_task_creation.py`: Task creation and label parsing tests
- `test_cli_commands.py`: CLI command integration tests
- `conftest.py`: Shared fixtures and mocks

**Mock Setup**:
- MSAL authentication flow
- Graph API responses (plans, buckets, task creation)
- File system operations for config/cache

**Key Test Scenarios**:

**Authentication Tests**:
- Successful device code flow
- Token caching and retrieval
- Error handling for auth failures

**Configuration Tests**:
- Config file loading with defaults
- Config saving with proper permissions
- Precedence: CLI args > env vars > config file
- Missing config error handling

**Resolution Tests**:
- GUID format detection
- Case-insensitive name matching
- Single match returns object
- Multiple matches raise Ambiguous error with candidates
- No matches raise NotFound error with candidates

**Task Creation Tests**:
- Label CSV parsing to category format
- Payload building with all optional fields
- Due date formatting to ISO string
- Description handling via details API

**CLI Integration Tests**:
- Command argument parsing
- JSON output format
- Error output and exit codes
- Environment variable resolution

**Test Data**: Use realistic test data for plans, buckets, and Graph API responses.

**Running Tests**: `pytest` with coverage reporting and verbose output.
