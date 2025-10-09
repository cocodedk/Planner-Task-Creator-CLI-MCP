# FAQ

## Do I need to pay for Azure?

**No!** Azure AD (Microsoft Entra ID) is included with:
- Microsoft 365 subscriptions
- Free Microsoft 365 Developer Program
- Most work/school accounts

You're only accessing Azure AD for app registration, not using Azure cloud services.

## What's the difference between Azure subscription and Azure AD?

- **Azure Subscription**: Paid cloud services (VMs, databases, etc.)
- **Azure AD**: Identity management (free with Microsoft 365)

This tool only needs Azure AD, not an Azure subscription!

## Can I use this with a free Microsoft account?

Not directly. Free Microsoft accounts don't have access to Azure AD app registrations.

**Solution:** Sign up for the free Microsoft 365 Developer Program.

## How long is the Developer Program free for?

- Initially 90 days
- Renewable every 90 days if you're actively using it
- Completely free for development/testing

## I get "No subscriptions found" in Azure Portal - is that okay?

**Yes!** You don't need a subscription. Just navigate to:
- **Azure Active Directory** → **App registrations**

This is available even without a subscription.

## My organization blocks app registrations - what can I do?

1. Ask your IT admin to register the app for you
2. Or use Developer Program with a personal developer tenant
3. Provide IT with the app permissions required (see [SETUP_GUIDE.md](../SETUP_GUIDE/azure-ad-setup.md))

## Can I use this for production?

The Developer Program is for development/testing. For production:
- Use your organization's Microsoft 365 account
- Or purchase a Microsoft 365 Business subscription ($6-20/month)
- Azure subscription still not required!
