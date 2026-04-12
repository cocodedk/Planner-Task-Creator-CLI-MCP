# CLAUDE.md — Planner Task Creator CLI MCP

## Project Overview

Planner Task Creator CLI MCP is a command-line tool and MCP server for creating and managing Microsoft Planner tasks. It provides both a standalone Python CLI and a Node.js/TypeScript MCP server wrapper for AI assistant integration, using Microsoft Graph API with OAuth2 device code flow.

- **Language / Runtime**: TypeScript (Node.js 20) + Python 3.12
- **Framework**: MCP SDK (Node.js), Typer + Rich (Python CLI)
- **Architecture**: Dual-runtime — TypeScript MCP server + Python business logic
- **Package / Namespace**: `planner-mcp-server`

---

## Required Skills — ALWAYS Invoke These

These skills **must** be invoked when the relevant situation arises. Never skip them.

| Situation | Skill |
|-----------|-------|
| Before any new feature or screen | `superpowers:brainstorming` |
| Planning multi-step changes | `superpowers:writing-plans` |
| Writing or fixing core logic | `superpowers:test-driven-development` |
| First sign of a bug or failure | `superpowers:systematic-debugging` |
| Before completing a feature branch | `superpowers:requesting-code-review` |
| Before claiming any task done | `superpowers:verification-before-completion` |
| Working on UI / frontend | `frontend-design:frontend-design` |
| After implementing — reviewing quality | `simplify` |

---

## Architecture

```
Planner Task Creator CLI MCP/
├── src/                 # TypeScript MCP server source
│   └── server/          # MCP handlers and tools
├── dist/                # Compiled TypeScript output
├── planner_lib/         # Python business logic library
├── planner.py           # Python CLI entry point
├── tests/               # Python unit tests
├── scripts/             # Setup and utility scripts
└── .github/workflows/   # CI, release, Pages automation
```

### Layer Rules
- TypeScript server delegates to Python via subprocess
- Python library must not depend on TypeScript
- OAuth tokens are cached locally and never committed

---

## Coding Conventions

- TypeScript strict mode — no `any` without justification
- All models are immutable — use copies for mutations
- Functions are pure where possible — no hidden side effects
- No hardcoded credentials — use environment variables or token cache
- 200-line maximum per file

---

## Engineering Principles

### File Size
- **200-line maximum per file** — extract a class, function, or module when approaching the limit

### DRY / SOLID / KISS / YAGNI
- Extract shared logic into named utilities; never copy-paste
- Single Responsibility: one class/function does one thing
- Don't add features not yet needed
- Delete dead code immediately

### TDD
- Write the failing test first, make it pass, then refactor
- Test names describe behaviour: `"should create task with due date"`
- One assertion per test — keep tests focused and readable

### Commit hygiene
- Follow Conventional Commits: `feat: ...` / `fix: ...` / `chore: ...`
- The `commit-msg` hook enforces this automatically

---

## Build Commands

```bash
npm run build     # Compile TypeScript
npm run dev       # Build and start dev server
npm start         # Start production MCP server
pytest            # Run Python tests
```

---

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file — project conventions and session startup |
| `version.txt` | Semantic version (MAJOR.MINOR.PATCH) |
| `.github/workflows/` | CI, release, and Pages automation |
| `.githooks/` | Pre-commit and commit-msg hooks |
| `scripts/install-hooks.sh` | One-time hook installer |

---

## Starting a New Session

1. Read this file
2. Run `npm run build && pytest` to confirm everything passes
3. Invoke `superpowers:brainstorming` before touching any feature
4. Follow the Required Skills table — every skill is mandatory, not optional
