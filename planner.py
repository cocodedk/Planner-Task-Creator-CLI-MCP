#!/usr/bin/env python3
"""
Microsoft Planner Task Creator CLI
A command-line tool for creating and managing Microsoft Planner tasks.

This is the main entry point that registers all commands from the modular planner_lib.
"""

import typer
from planner_lib.cli_commands import register_all_commands
from planner_lib.cli_task_commands import register_task_commands
from planner_lib.cli_bucket_commands import register_bucket_commands

# Initialize CLI app
app = typer.Typer(help="Microsoft Planner Task Creator CLI")

# Register all commands
register_all_commands(app)
register_task_commands(app)
register_bucket_commands(app)

if __name__ == "__main__":
    app()
