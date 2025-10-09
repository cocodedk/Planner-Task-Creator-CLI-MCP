# Microsoft 365 Developer Program (Recommended)

Get a **free** Microsoft 365 developer tenant with Azure AD included!

## Step 1: Sign Up for Developer Program

1. Go to [Microsoft 365 Developer Program](https://developer.microsoft.com/en-us/microsoft-365/dev-program)
2. Click **Join Now** (it's free)
3. Sign in with your Microsoft account (or create one)
4. Fill out the profile form

## Step 2: Set Up Your Developer Tenant

1. After joining, you'll get a **free Microsoft 365 E5 subscription** (renewable every 90 days)
2. This includes:
   - Azure AD (Microsoft Entra ID)
   - Microsoft Planner
   - 25 user licenses
3. Choose a domain name (e.g., `yourname.onmicrosoft.com`)

## Step 3: Access Azure AD

1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your developer account
3. You'll see **Azure Active Directory** in the left menu
4. **No Azure subscription needed!** Azure AD is included with Microsoft 365

## Step 4: Register Your App

Follow the [SETUP_GUIDE.md](../SETUP_GUIDE/azure-ad-setup.md) instructions, but note:

- You're the admin, so you can grant admin consent
- Use the permissions listed in the Azure AD setup guide
- The `User.Read.All` permission is required for task assignment

## Step 5: Set Up Planner

1. Go to [Microsoft Planner](https://tasks.office.com)
2. Sign in with your developer account
3. Create a test plan and bucket

## Step 6: Use the CLI

```bash
# Configure
export TENANT_ID="your-tenant-id-from-app-registration"
export CLIENT_ID="your-client-id-from-app-registration"

# Authenticate
python planner.py init-auth

# Test it
python planner.py list-plans
```
