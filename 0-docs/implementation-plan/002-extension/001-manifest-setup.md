# 002-extension/001: Extension Manifest Configuration

## Goal
Create Chrome extension manifest v3 with minimal required permissions.

## Steps

1. **Create manifest.json** in `extension/public/`

2. **Configure basic metadata**
   - Name: "PlannerAgent"
   - Version: 0.1.0
   - Description: AI-driven Microsoft Planner integration
   - Manifest version: 3

3. **Define host permissions** (minimum required)
   - `https://tasks.office.com/*` (Planner UI)
   - `https://*.microsoft.com/*` (Microsoft auth/APIs)

4. **Configure background service worker**
   - Script: `background.js`
   - Type: module

5. **Configure content scripts**
   - Matches: `https://tasks.office.com/*`
   - Scripts: `content.js`
   - Run at: `document_idle`

6. **Set permissions**
   - `storage` (for caching state)
   - `activeTab` (for UI interaction)

7. **Configure icons** (placeholder for now)
   - 16x16, 48x48, 128x128 PNG

## Acceptance Criteria

- [ ] manifest.json valid and loads in Chrome
- [ ] Minimum permissions only
- [ ] Background and content scripts configured
- [ ] Matches Planner URLs correctly

## ⚠️ File Size Reminder
**All source files created must be under 200 lines. NO EXCEPTIONS.**

## Dependencies
- Completes after: 001-setup/002-extension-dependencies

## Time Estimate
30 minutes

## Security Notes
- Start with minimal permissions
- Add more only when proven necessary
- Document why each permission is needed
