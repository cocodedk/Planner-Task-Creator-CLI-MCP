# Quick Start Guide

Get up and running with the Planner CLI in 5 minutes.

## Prerequisites

- Python 3.8+
- Azure AD app registration
  - **No Azure subscription needed!** See [SETUP_WITHOUT_AZURE_SUBSCRIPTION.md](SETUP_WITHOUT_AZURE_SUBSCRIPTION.md)
  - Free option: [Microsoft 365 Developer Program](https://developer.microsoft.com/en-us/microsoft-365/dev-program)
- Access to Microsoft Planner

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure

Create `~/.planner-cli/config.json`:

```bash
mkdir -p ~/.planner-cli
cat > ~/.planner-cli/config.json << 'EOF'
{
  "tenant_id": "YOUR-TENANT-ID",
  "client_id": "YOUR-CLIENT-ID"
}
EOF
chmod 600 ~/.planner-cli/config.json
```

## 3. Authenticate

```bash
python planner.py init-auth
```

Follow the device code instructions in your browser.

## 4. Set Defaults

```bash
python planner.py set-defaults --plan "YOUR-PLAN-NAME" --bucket "To Do"
```

## 5. Create Your First Task

```bash
python planner.py add --title "My first task"
```

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Check [EXAMPLES.md](EXAMPLES.md) for more usage examples
- Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete Azure AD setup
- Run tests: `pytest`

## Common Commands

```bash
# List your plans
python planner.py list-plans

# List buckets in a plan
python planner.py list-buckets --plan "My Plan"

# Create task with details
python planner.py add \
  --title "Task title" \
  --desc "Description" \
  --due "2024-12-31" \
  --labels "Label1,Label2"
```

## Need Help?

- Check the [Troubleshooting](README.md#troubleshooting) section
- Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
- See [EXAMPLES.md](EXAMPLES.md) for usage patterns
