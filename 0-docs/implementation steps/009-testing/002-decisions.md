# Testing Module Decisions

**Framework**: Use `pytest` for Python testing.

**Test Structure**:
- Unit tests for individual functions
- Integration tests for CLI commands
- Mock external dependencies (MSAL, Graph API)

**Mock Strategy**:
- Mock `msal.PublicClientApplication` for auth tests
- Mock `requests` for Graph API tests
- Use test fixtures for config and token data

**Test Coverage**:
- Authentication token acquisition and caching
- Configuration loading, saving, and resolution
- Plan and bucket name/ID resolution
- Label parsing and task creation payload building
- CLI command argument parsing and output formatting
- Error handling and JSON error responses

**Test Matrix** (from PRD):
- Auth flow shows device code and succeeds
- Defaults work for task creation
- Name resolution handles typos with candidates
- Ambiguous names show multiple candidates
- Missing scopes return proper error
