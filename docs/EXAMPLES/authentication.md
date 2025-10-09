# Authentication

## Standard Authentication Flow

```bash
$ python planner.py init-auth

Authentication Required
Please visit: https://microsoft.com/devicelogin
Enter code: ABC123XYZ

# After completing authentication in browser:
✓ Authentication successful!
```

## Using Environment Variables

```bash
export TENANT_ID="12345678-1234-1234-1234-123456789abc"
export CLIENT_ID="87654321-4321-4321-4321-cba987654321"

python planner.py init-auth
```

## Using Config File Only

```bash
# Create config file
cat > ~/.planner-cli/config.json << 'EOF'
{
  "tenant_id": "12345678-1234-1234-1234-123456789abc",
  "client_id": "87654321-4321-4321-4321-cba987654321"
}
EOF

chmod 600 ~/.planner-cli/config.json

# Authenticate
python planner.py init-auth
```
