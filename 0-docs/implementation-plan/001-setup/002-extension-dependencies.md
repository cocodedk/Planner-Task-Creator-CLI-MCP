# 001-setup/002: Extension Dependencies Setup

## Goal
Initialize TypeScript build environment for browser extension.

## Steps

1. **Create extension package.json**
   ```bash
   cd extension/
   npm init -y
   ```

2. **Install TypeScript and build tools**
   ```bash
   npm install --save-dev typescript @types/chrome
   npm install --save-dev esbuild
   ```

3. **Create tsconfig.json**
   - Target ES2020
   - Module ESNext
   - Include Chrome types
   - Strict mode enabled
   - Output to `dist/`

4. **Create build script** in `scripts/build-extension.sh`
   - Use esbuild for bundling
   - Separate bundles for background and content scripts
   - Development and production modes

5. **Add npm scripts** to package.json
   - `build`: Production build
   - `build:dev`: Development build with source maps
   - `watch`: Watch mode for development

## Acceptance Criteria

- [ ] package.json configured
- [ ] TypeScript dependencies installed
- [ ] tsconfig.json with strict settings
- [ ] Build script works (can run `npm run build`)

## ⚠️ File Size Reminder
**All source files created must be under 200 lines. NO EXCEPTIONS.**

## Dependencies
- Completes after: 001-project-structure

## Time Estimate
30 minutes
