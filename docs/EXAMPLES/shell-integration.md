# Shell Integration

## Bash Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc

alias planner='python ~/.planner-cli/planner.py'
alias ptask='python ~/.planner-cli/planner.py add --title'
alias plist='python ~/.planner-cli/planner.py list-plans'
alias pbuckets='python ~/.planner-cli/planner.py list-buckets'

# Usage:
# ptask "Quick task"
# plist
# pbuckets --plan "Work"
```

## Fish Shell Functions

```fish
# Add to ~/.config/fish/functions/

# Function: planner.fish
function planner
    python ~/.planner-cli/planner.py $argv
end

# Function: ptask.fish
function ptask
    python ~/.planner-cli/planner.py add --title $argv
end

# Usage:
# ptask "Quick task"
# planner list-plans
```

## ZSH Completion (Basic)

```zsh
# Add to ~/.zshrc

_planner() {
  local commands
  commands=(
    'init-auth:Initialize authentication'
    'set-defaults:Set default plan and bucket'
    'list-plans:List all plans'
    'list-buckets:List buckets in a plan'
    'add:Create a new task'
  )

  _describe 'command' commands
}

compdef _planner planner
```
