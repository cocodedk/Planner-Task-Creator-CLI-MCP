# CLI Installation

## Step 1: Get the Code

### Option A: Clone Repository
```bash
cd ~/projects
git clone <repo-url> planner-cli
cd planner-cli
```

### Option B: Download Files
If you have the files already, just navigate to the directory.

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or with a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 3: Configure the CLI

### Option A: Environment Variables
Add to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:

```bash
export TENANT_ID="your-tenant-id-here"
export CLIENT_ID="your-client-id-here"
export PLANNER_DEFAULT_PLAN="My Plan Name"  # Optional
export PLANNER_DEFAULT_BUCKET="To Do"       # Optional
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Option B: Config File
```bash
mkdir -p ~/.planner-cli

cat > ~/.planner-cli/config.json << 'EOF'
{
  "tenant_id": "your-tenant-id-here",
  "client_id": "your-client-id-here",
  "default_plan": "My Plan Name",
  "default_bucket": "To Do"
}
EOF

chmod 600 ~/.planner-cli/config.json
```

## Step 4: Make CLI Accessible

### Option A: Direct execution
```bash
chmod +x planner.py
```

### Option B: System-wide access
```bash
# Create directory
mkdir -p ~/.planner-cli

# Copy CLI
cp planner.py ~/.planner-cli/

# Create symlink
sudo ln -s ~/.planner-cli/planner.py /usr/local/bin/planner

# Now you can run: planner --help
```
