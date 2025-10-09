# Security Best Practices

## ✅ DO:
- ✅ Keep credentials in `~/.config/Cursor/mcp.json` (not in repo)
- ✅ Use `.env` file for local development (already in `.gitignore`)
- ✅ Use `.env.example` as a template (safe to commit)
- ✅ Set file permissions: `chmod 600 ~/.config/Cursor/mcp.json`

## ❌ DON'T:
- ❌ Commit `.env` files to git
- ❌ Hardcode credentials in scripts
- ❌ Share your `mcp.json` file publicly
- ❌ Include credentials in documentation
