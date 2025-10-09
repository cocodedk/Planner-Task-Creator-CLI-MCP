# CLI Commands Module Decisions

**Framework**: Use `typer` for CLI with automatic help generation and type conversion.

**Output**: Use `rich` for colored output, JSON for machine-readable errors and results.

**Command Structure**:
- `init-auth`: Initialize authentication (no args)
- `set-defaults --plan PLAN --bucket BUCKET`: Save defaults to config
- `list-plans`: List user's plans as JSON
- `list-buckets --plan PLAN`: List buckets for specific plan as JSON
- `add`: Main task creation command with all options

**Error Output**: Always output structured JSON errors for programmatic consumption.

**Exit Codes**: Use typer.Exit(2) for configuration errors, let other errors propagate.
