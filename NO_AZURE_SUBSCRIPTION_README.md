# 🎉 You Don't Need an Azure Subscription!

## TL;DR

✅ **Azure AD (Microsoft Entra ID) is FREE**
✅ **No Azure subscription required**
✅ **Just need a Microsoft 365 account**

## Three Ways to Get Started (All Free!)

### Option 1: Work/School Account (Easiest if you have one)
- Use your existing work/school Microsoft 365 account
- Ask your IT admin to register an app for you
- Takes 10 minutes with admin help

### Option 2: Microsoft 365 Developer Program (Best for Testing) ⭐
- **Completely free** developer tenant
- Get a free Microsoft 365 E5 subscription
- You're the admin - full control
- Includes Azure AD + Planner + 25 user licenses
- Renewable every 90 days

**Sign up:** https://developer.microsoft.com/en-us/microsoft-365/dev-program

### Option 3: Personal Microsoft Account (Limited)
- Personal accounts have limited Azure AD access
- Not recommended - use Option 2 instead

## What You Get for Free

With the Microsoft 365 Developer Program:

```
✅ Microsoft 365 E5 Subscription
✅ Azure AD (Microsoft Entra ID)
✅ Microsoft Planner
✅ 25 user licenses
✅ Sample data for testing
✅ Your own domain: [yourname].onmicrosoft.com
✅ Full admin rights
✅ No credit card required
✅ 90-day renewable subscription
```

## Quick Setup (5 Minutes)

### Step 1: Get Your Free Developer Tenant

1. Visit: https://developer.microsoft.com/en-us/microsoft-365/dev-program
2. Click "Join Now"
3. Sign in with any Microsoft account
4. Set up your E5 subscription
5. Choose domain: `[yourname].onmicrosoft.com`
6. Wait 1-2 minutes

### Step 2: Access Azure AD (No Subscription Needed!)

1. Go to: https://portal.azure.com
2. Sign in with your developer account
3. Find "Azure Active Directory" in left menu
4. No Azure subscription required!

### Step 3: Register the App

1. **Azure Active Directory** → **App registrations** → **New registration**
2. Name: `Planner Task Creator CLI`
3. Redirect URI: `http://localhost` (Public client)
4. Click **Register**
5. Copy your **Tenant ID** and **Client ID**

### Step 4: Add Permissions

1. **API permissions** → **Add a permission**
2. **Microsoft Graph** → **Delegated permissions**
3. Add: `Tasks.ReadWrite`, `Group.ReadWrite.All`, `offline_access`
4. Click **Grant admin consent**

### Step 5: Enable Public Client

1. **Authentication** → **Advanced settings**
2. **Allow public client flows**: Set to **Yes**
3. Save

### Step 6: Use the CLI!

```bash
export TENANT_ID="your-tenant-id"
export CLIENT_ID="your-client-id"

python planner.py init-auth
python planner.py list-plans
python planner.py add --title "My first task"
```

## Why This Works

**Azure AD ≠ Azure Subscription**

- **Azure Subscription**: Paid cloud services (VMs, databases, storage)
- **Azure AD**: Identity management (FREE with Microsoft 365)

This tool only needs Azure AD for:
- ✅ App registration (free)
- ✅ OAuth authentication (free)
- ✅ API permissions (free)

You never touch paid Azure services!

## Common Questions

### "But I see 'No subscriptions found' in Azure Portal?"

**That's fine!** You don't need an Azure subscription. Just navigate to:
- **Azure Active Directory** (in left menu or search bar)
- This is always free with Microsoft 365

### "How long is the Developer Program free?"

- **90 days initially**
- **Renewable every 90 days** if you're actively using it
- **Completely free** - no credit card ever required

### "Can I use this for production?"

The Developer Program is for development/testing. For production:
- Use your organization's Microsoft 365 account
- Or purchase a Microsoft 365 Business subscription ($6-20/month)
- Azure subscription still not required!

### "What if my organization blocks app registrations?"

Two options:
1. Ask your IT admin to register the app
2. Use a separate developer tenant for personal use

## Full Documentation

For detailed step-by-step instructions:

📖 **[SETUP_WITHOUT_AZURE_SUBSCRIPTION.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION.md)**

This includes:
- Screenshots and walkthroughs
- Troubleshooting common issues
- Alternative options
- Complete setup instructions

## Next Steps

1. ⭐ **[Join Microsoft 365 Developer Program](https://developer.microsoft.com/en-us/microsoft-365/dev-program)** (5 min)
2. 📖 Read **[SETUP_WITHOUT_AZURE_SUBSCRIPTION.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION.md)** (detailed guide)
3. 🚀 Follow **[QUICKSTART.md](QUICKSTART.md)** (install CLI)
4. ✅ Start creating tasks!

## Resources

- [Microsoft 365 Developer Program](https://developer.microsoft.com/en-us/microsoft-365/dev-program)
- [Azure AD Free Features](https://azure.microsoft.com/en-us/pricing/details/active-directory/)
- [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)

---

**Remember:** Azure AD is free with Microsoft 365. No Azure subscription needed! 🎉
