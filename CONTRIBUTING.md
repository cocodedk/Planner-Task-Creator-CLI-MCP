# Contributing to Planner Task Creator CLI MCP

## Local Setup
1. Install Node.js 20+ and Python 3.12+.
2. Clone the repository: `git clone https://github.com/cocodedk/Planner-Task-Creator-CLI-MCP`
3. Install Node dependencies: `npm install`
4. Install Python dependencies: `pip install -r requirements.txt`
5. Build TypeScript: `npm run build`

## Install Git Hooks
```sh
./scripts/install-hooks.sh
```

## Local Git Setup
Run these once after cloning:
```bash
git config pull.rebase true
git config core.autocrlf input
git config push.autoSetupRemote true
git config init.defaultBranch main
```

## Build and Test Commands
```bash
npm run build     # Compile TypeScript
npm run dev       # Build and start dev server
pytest            # Run Python tests
```

## Coding Style
- TypeScript strict mode — no `any` without justification.
- Follow existing Python and TypeScript conventions.
- Keep files small and focused (200-line maximum).
- Use Conventional Commits for all commit messages.

## Branch Naming
| Prefix | Use for |
|--------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `chore/` | Maintenance |
| `docs/` | Documentation |
| `ci/` | CI changes |

## PR Checklist
- [ ] Build passes (`npm run build`).
- [ ] Python tests pass (`pytest`).
- [ ] Manual test completed for changed functionality.
- [ ] Updated docs if behaviour changed.
- [ ] Commit messages follow Conventional Commits.
