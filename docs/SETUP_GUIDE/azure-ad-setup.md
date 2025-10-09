# Azure AD App Registration

## Step 1: Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in:
   - **Name**: `Planner Task Creator CLI`
   - **Supported account types**: Choose based on your needs
   - **Redirect URI**: Select "Public client/native" and enter `http://localhost`
5. Click **Register**

## Step 2: Note Your IDs

After registration, note these values:
- **Application (client) ID**: Found on the Overview page
- **Directory (tenant) ID**: Found on the Overview page

## Step 3: Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph** → **Delegated permissions**
4. Add these permissions:
   - `Tasks.ReadWrite` - Read and write user and shared tasks
   - `Group.ReadWrite.All` - Read and write all groups (requires admin consent)
   - `User.Read.All` - Read all users' full profiles (requires admin consent)
   - `User.ReadBasic.All` - Read all users' basic profiles (optional)
5. Click **Add permissions**
6. Click **Grant admin consent** (if you have admin rights)

**Important Notes:**
- `Group.ReadWrite.All` requires admin consent for accessing plans and buckets
- `User.Read.All` or `User.ReadBasic.All` is **required for task assignment by email**
- Without `User.Read.All`, you can only assign tasks using User IDs (GUIDs)
- Admin consent is required for `User.Read.All` - without it, user lookups will fail
- You can still use the tool with just `Tasks.ReadWrite` for basic task creation (without assignments)

## Step 4: Configure Authentication

1. Go to **Authentication** in your app registration
2. Under **Advanced settings** → **Allow public client flows**: Set to **Yes**
3. Click **Save**
