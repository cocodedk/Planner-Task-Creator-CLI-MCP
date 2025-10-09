# Detailed Developer Program Walkthrough

## 1. Join the Program

```
Visit: https://developer.microsoft.com/en-us/microsoft-365/dev-program
→ Click "Join Now"
→ Sign in with Microsoft account
→ Complete profile form
→ Wait for approval (usually instant)
```

## 2. Set Up Developer Tenant

```
→ After approval, click "Set up E5 subscription"
→ Choose your admin username
→ Choose domain: [yourname].onmicrosoft.com
→ Create password
→ Add phone number (for security)
→ Wait 1-2 minutes for tenant setup
```

## 3. Access Your Tenant

```
Admin email: admin@[yourname].onmicrosoft.com
Password: [your-password]
Tenant: [yourname].onmicrosoft.com
```

## 4. Access Azure Portal

```
Visit: https://portal.azure.com
→ Sign in with: admin@[yourname].onmicrosoft.com
→ You'll see Azure AD (no subscription needed!)
```

## 5. Register App

```
→ Azure Active Directory
→ App registrations
→ New registration
→ Name: Planner Task Creator CLI
→ Redirect URI: http://localhost (Public client)
→ Register
```

## 6. Get Your IDs

```
On Overview page:
→ Copy "Application (client) ID"
→ Copy "Directory (tenant) ID"
```

## 7. Add Permissions

```
→ API permissions
→ Add a permission
→ Microsoft Graph
→ Delegated permissions
→ Add: Tasks.ReadWrite, Group.ReadWrite.All, User.Read.All
→ Grant admin consent for [your tenant]
```

## 8. Enable Public Client

```
→ Authentication
→ Advanced settings
→ Allow public client flows: Yes
→ Save
```

## 9. Test with CLI

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
