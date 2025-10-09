# Setup Without Azure Subscription

**Good news!** You don't need an Azure subscription to use this tool. You only need:

1. A Microsoft 365 account (work, school, or personal with Microsoft 365)
2. Access to Microsoft Planner
3. Azure AD (Microsoft Entra ID) - available for free

## Option 1: Use Your Organization's Azure AD (Recommended)

If you have a work or school Microsoft 365 account:

### Step 1: Check Your Access

1. Go to [Microsoft 365 Admin Center](https://admin.microsoft.com)
2. If you see a dashboard, you have an organization account
3. Your organization already has Azure AD set up

### Step 2: Register the App (Need Admin Help)

**If you're an admin:**
1. Go to [Azure Portal](https://portal.azure.com) (free to access)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Follow the [SETUP_GUIDE.md](SETUP_GUIDE.md#step-1-azure-ad-app-registration) instructions

**If you're not an admin:**
1. Ask your IT admin to create an app registration for you
2. Request these specific permissions:
   - `Tasks.ReadWrite` (delegated)
   - `Group.ReadWrite.All` (delegated - requires admin consent)
3. They'll give you the `Tenant ID` and `Client ID`

### Step 3: Use the CLI

Once you have the Tenant ID and Client ID, you can use the CLI:

```bash
export TENANT_ID="your-tenant-id"
export CLIENT_ID="your-client-id"

python planner.py init-auth
```

## Option 2: Use Microsoft 365 Developer Program (Free)

Get a **free** Microsoft 365 developer tenant with Azure AD included!

### Step 1: Sign Up for Developer Program

1. Go to [Microsoft 365 Developer Program](https://developer.microsoft.com/en-us/microsoft-365/dev-program)
2. Click **Join Now** (it's free)
3. Sign in with your Microsoft account (or create one)
4. Fill out the profile form

### Step 2: Set Up Your Developer Tenant

1. After joining, you'll get a **free Microsoft 365 E5 subscription** (renewable every 90 days)
2. This includes:
   - Azure AD (Microsoft Entra ID)
   - Microsoft Planner
   - 25 user licenses
3. Choose a domain name (e.g., `yourname.onmicrosoft.com`)

### Step 3: Access Azure AD

1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your developer account
3. You'll see **Azure Active Directory** in the left menu
4. **No Azure subscription needed!** Azure AD is included with Microsoft 365

### Step 4: Register Your App

Now follow the standard setup:

1. In Azure Portal, go to **Azure Active Directory** → **App registrations**
2. Click **New registration**
3. Name: `Planner Task Creator CLI`
4. Redirect URI: `http://localhost` (Public client/native)
5. Click **Register**
6. Note your **Application (client) ID** and **Directory (tenant) ID**

### Step 5: Configure Permissions

1. Go to **API permissions** in your app
2. Click **Add a permission** → **Microsoft Graph** → **Delegated permissions**
3. Add:
   - `Tasks.ReadWrite`
   - `Group.ReadWrite.All`
4. Click **Grant admin consent** (you're the admin!)

**Note:** The `offline_access` scope is automatically included by MSAL and doesn't need to be added explicitly.

### Step 6: Enable Public Client Flow

1. Go to **Authentication** in your app
2. Under **Advanced settings** → **Allow public client flows**: Set to **Yes**
3. Click **Save**

### Step 7: Set Up Planner

1. Go to [Microsoft Planner](https://tasks.office.com)
2. Sign in with your developer account
3. Create a test plan and bucket

### Step 8: Use the CLI

```bash
# Configure
export TENANT_ID="your-tenant-id-from-app-registration"
export CLIENT_ID="your-client-id-from-app-registration"

# Authenticate
python planner.py init-auth

# Test it
python planner.py list-plans
```

## Option 3: Personal Microsoft Account (Limited)

If you have a personal Microsoft account with Microsoft 365 subscription:

### Limitations

- Personal Microsoft accounts have limited Azure AD capabilities
- You may not be able to register apps
- **Recommendation:** Use Option 2 (Developer Program) instead

### What You Can Try

1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your personal Microsoft account
3. If you see "No subscriptions found" - that's okay!
4. Look for **Azure Active Directory** in the left menu
5. If it's not available, use Option 2 (Developer Program)

## Comparing Options

| Option | Cost | Setup Time | Best For |
|--------|------|------------|----------|
| **Work/School Account** | Free | 10 min (with admin) | Active employees/students |
| **Developer Program** | Free | 15 min | Developers, testing, learning |
| **Personal Account** | Limited | N/A | Not recommended |

## FAQ

### Do I need to pay for Azure?

**No!** Azure AD (Microsoft Entra ID) is included with:
- Microsoft 365 subscriptions
- Free Microsoft 365 Developer Program
- Most work/school accounts

You're only accessing Azure AD for app registration, not using Azure cloud services.

### What's the difference between Azure subscription and Azure AD?

- **Azure Subscription**: Paid cloud services (VMs, databases, etc.)
- **Azure AD**: Identity management (free with Microsoft 365)

This tool only needs Azure AD, not an Azure subscription!

### Can I use this with a free Microsoft account?

Not directly. Free Microsoft accounts don't have access to Azure AD app registrations.

**Solution:** Sign up for the free Microsoft 365 Developer Program (Option 2).

### How long is the Developer Program free for?

- Initially 90 days
- Renewable every 90 days if you're actively using it
- Completely free for development/testing

### I get "No subscriptions found" in Azure Portal - is that okay?

**Yes!** You don't need an Azure subscription. You just need to access:
- **Azure Active Directory** → **App registrations**

This is available even without a subscription.

### My organization blocks app registrations - what can I do?

1. Ask your IT admin to register the app for you
2. Or use Option 2 (Developer Program) with a personal developer tenant
3. Provide IT with the app permissions required (see above)

## Detailed: Developer Program Setup

### Complete Walkthrough

**1. Join the Program**
```
Visit: https://developer.microsoft.com/en-us/microsoft-365/dev-program
→ Click "Join Now"
→ Sign in with Microsoft account
→ Complete profile form
→ Wait for approval (usually instant)
```

**2. Set Up Developer Tenant**
```
→ After approval, click "Set up E5 subscription"
→ Choose your admin username
→ Choose domain: [yourname].onmicrosoft.com
→ Create password
→ Add phone number (for security)
→ Wait 1-2 minutes for tenant setup
```

**3. Access Your Tenant**
```
Admin email: admin@[yourname].onmicrosoft.com
Password: [your-password]
Tenant: [yourname].onmicrosoft.com
```

**4. Access Azure Portal**
```
Visit: https://portal.azure.com
→ Sign in with: admin@[yourname].onmicrosoft.com
→ You'll see Azure AD (no subscription needed!)
```

**5. Register App**
```
→ Azure Active Directory
→ App registrations
→ New registration
→ Name: Planner Task Creator CLI
→ Redirect URI: http://localhost (Public client)
→ Register
```

**6. Get Your IDs**
```
On Overview page:
→ Copy "Application (client) ID"
→ Copy "Directory (tenant) ID"
```

**7. Add Permissions**
```
→ API permissions
→ Add a permission
→ Microsoft Graph
→ Delegated permissions
→ Add: Tasks.ReadWrite, Group.ReadWrite.All
→ Grant admin consent for [your tenant]
```

**8. Enable Public Client**
```
→ Authentication
→ Advanced settings
→ Allow public client flows: Yes
→ Save
```

**9. Test with CLI**
```bash
export TENANT_ID="your-directory-tenant-id"
export CLIENT_ID="your-application-client-id"

python planner.py init-auth
# Follow the device code flow
# You'll authenticate as admin@[yourname].onmicrosoft.com

python planner.py list-plans
```

## Getting Sample Data

With the Developer Program, you can populate sample data:

1. Go to [Microsoft 365 Admin Center](https://admin.microsoft.com)
2. Sign in with your developer account
3. **Setup** → **Sample data**
4. Install sample users and content
5. This will create sample plans in Planner

## Troubleshooting

### "You don't have permission to register applications"

**Solution:** You need to be an admin or use a developer tenant where you're the admin.

### "AADSTS50020: User account from identity provider does not exist"

**Solution:** Make sure you're using the correct tenant. Sign out and sign in with the right account.

### "No subscriptions found" in Azure Portal

**Solution:** This is normal! You don't need a subscription. Just navigate to **Azure Active Directory** from the left menu.

### Can't see Azure Active Directory in Azure Portal

**Solution:**
1. Use the search bar at the top
2. Type "Azure Active Directory"
3. Or use direct link: https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade

### "Insufficient privileges to complete the operation"

**Solution:** You need admin rights. Either:
- Use a developer tenant where you're the admin
- Ask your organization admin for help

## Summary

✅ **You don't need an Azure subscription!**

**Recommended path:**
1. Sign up for Microsoft 365 Developer Program (free)
2. Get a free E5 tenant with Azure AD included
3. Register the app in Azure AD (no subscription required)
4. Use the CLI with your developer tenant

**Alternative:**
- Use your work/school account (ask admin to register app)

## Next Steps

Once you have your Tenant ID and Client ID:

1. Follow [QUICKSTART.md](QUICKSTART.md) to install the CLI
2. Configure with your credentials
3. Start creating tasks!

## Resources

- [Microsoft 365 Developer Program](https://developer.microsoft.com/en-us/microsoft-365/dev-program)
- [Azure AD Documentation](https://docs.microsoft.com/en-us/azure/active-directory/)
- [App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Microsoft Graph Permissions](https://docs.microsoft.com/en-us/graph/permissions-reference)

---

**Need help?** The Microsoft 365 Developer Program is the easiest way to get started for free!
