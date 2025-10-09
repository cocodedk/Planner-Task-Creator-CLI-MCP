# File Structure

```
planner-task-creator-cli-mcp/
├── planner.py                 # Main Python CLI (650+ lines)
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
├── tsconfig.json             # TypeScript configuration
├── pytest.ini                # Test configuration
├── .gitignore               # Git ignore patterns
├── LICENSE                   # MIT license
│
├── src/
│   └── server.ts            # MCP server (250+ lines)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py         # Auth tests
│   ├── test_config.py       # Config tests
│   ├── test_resolution.py   # Resolution tests
│   ├── test_task_creation.py # Task tests
│   └── test_cli_commands.py  # CLI tests
│
├── 0-docs/
│   ├── prd.md               # Product requirements
│   └── implementation steps/ # Detailed specifications
│       ├── 000-overview.md
│       ├── 001-authentication/
│       ├── 002-graph-client/
│       ├── 003-configuration/
│       ├── 004-resolution/
│       ├── 005-task-creation/
│       ├── 006-cli-commands/
│       ├── 007-error-handling/
│       ├── 008-mcp-server/
│       └── 009-testing/
│
└── Documentation/
    ├── index/                # Main documentation index (refactored)
    ├── ARCHITECTURE/         # Architecture docs (refactored)
    ├── SETUP_GUIDE/          # Setup guide (refactored)
    ├── SETUP_WITHOUT_AZURE_SUBSCRIPTION/ # No subscription guide (refactored)
    ├── TEST_RESULTS/         # Test results (refactored)
    ├── PROJECT_SUMMARY/      # Project summary (refactored)
    ├── README.md             # Main docs
    ├── QUICKSTART.md         # Quick start
    ├── EXAMPLES.md           # Examples
    └── PROJECT_SUMMARY.md    # Summary
```
