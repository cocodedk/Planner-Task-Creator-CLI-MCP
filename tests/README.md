# Test Suite

## Test Configuration

### Environment Variables

The tests use environment variables to avoid hardcoding sensitive Azure AD User IDs.

**Setup:**

1. Copy `.env.example` to `.env` in the project root:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace the placeholder IDs with real Azure AD User GUIDs from your tenant:
   ```bash
   TEST_USER_ID_1=your-actual-user-guid-1
   TEST_USER_ID_2=your-actual-user-guid-2
   ```

3. **Never commit the `.env` file** - it's in `.gitignore` for security

### Test Helpers

The `test_helpers.py` module provides utility functions to safely access test data:

- `get_test_user_id_1()` - Returns TEST_USER_ID_1 from environment or a placeholder
- `get_test_user_id_2()` - Returns TEST_USER_ID_2 from environment or a placeholder

These functions ensure tests work even without a `.env` file (using placeholder IDs) but can use real IDs for integration testing when configured.

## Running Tests

```bash
# Run all tests
./venv/bin/pytest tests/ -v

# Run specific test file
./venv/bin/pytest tests/test_resolution_users.py -v

# Run with coverage
./venv/bin/pytest tests/ --cov=planner_lib
```

## Test Organization

- `conftest.py` - Shared fixtures and mocks
- `test_helpers.py` - Utility functions for test data
- `test_*.py` - Test modules organized by feature
- `test_*/__init__.py` - Test subpackages for complex features

## Security Notes

- Never commit real Azure AD User IDs to the repository
- Use the helper functions from `test_helpers.py` for all user ID references
- The `.env` file is gitignored and should remain local only
- The `.env.example` file shows the structure but uses placeholder values
