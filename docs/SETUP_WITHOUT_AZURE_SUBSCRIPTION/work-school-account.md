# Work/School Account Setup

If you have a work or school Microsoft 365 account:

## Step 1: Check Your Access

1. Go to [Microsoft 365 Admin Center](https://admin.microsoft.com)
2. If you see a dashboard, you have an organization account
3. Your organization already has Azure AD set up

## Step 2: Register the App (Need Admin Help)

**If you're an admin:**
1. Go to [Azure Portal](https://portal.azure.com) (free to access)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Follow the [SETUP_GUIDE.md](../SETUP_GUIDE/azure-ad-setup.md) instructions

**If you're not an admin:**
1. Ask your IT admin to create an app registration for you
2. Request these specific permissions:
   - `Tasks.ReadWrite` (delegated)
   - `Group.ReadWrite.All` (delegated - requires admin consent)
   - `User.Read.All` (delegated - requires admin consent)
3. They'll give you the `Tenant ID` and `Client ID`

## Step 3: Use the CLI

Once you have the Tenant ID and Client ID, you can use the CLI:

```bash
export TENANT_ID="your-tenant-id"
export CLIENT_ID="your-client-id"

python planner.py init-auth
```
