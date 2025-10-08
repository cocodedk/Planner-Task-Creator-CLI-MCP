# 008-integration/004: User Documentation

## Goal
Create minimal user documentation for setup and usage.

## Documents to Create

### 1. README.md (root)
```markdown
- Project overview
- Architecture diagram (text/ASCII)
- Quick start guide
- Prerequisites
- Installation steps
- Troubleshooting
```

### 2. SETUP.md
```markdown
- Detailed setup instructions
- Chrome extension installation
- MCP server installation
- Configuration
- Verifying installation
```

### 3. USAGE.md
```markdown
- How to use with AI agent
- Example commands
- Supported operations
- Limitations
- FAQ
```

### 4. DEVELOPMENT.md
```markdown
- Development setup
- Project structure
- Building from source
- Testing
- Debugging tips
```

### 5. API.md
```markdown
- MCP tool reference
- Input schemas
- Output schemas
- Error codes
- Examples
```

## Documentation Principles

- **Concise**: Bullet points, no long prose
- **Actionable**: Every doc has clear next steps
- **Examples**: Show don't tell
- **Up-to-date**: Document current state, not plans

## Screenshot/Diagrams

Create simple diagrams:
- Architecture flow (text-based)
- Message sequence diagrams
- Setup process flowchart

## Acceptance Criteria

- [ ] All documentation files created
- [ ] Setup guide tested by following steps
- [ ] Usage examples tested and working
- [ ] API reference complete
- [ ] Troubleshooting section covers common issues

## ⚠️ File Size Reminder
**Ensure all code examples in docs respect 200-line limit.**

## Dependencies
- Completes after: 008-integration/003-performance-testing

## Time Estimate
2-3 hours

## Notes
Keep documentation in 0-docs/ during development.
Copy to root for final release.
