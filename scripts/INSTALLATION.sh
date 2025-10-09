#!/bin/bash
# Installation script for Planner Task Creator CLI + MCP Server

set -e  # Exit on error

echo "=========================================="
echo "Planner Task Creator CLI + MCP Server"
echo "Installation Script"
echo "=========================================="
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or later from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check Node.js (optional)
echo
echo "Checking Node.js installation (for MCP server)..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
    INSTALL_MCP=true
else
    echo -e "${YELLOW}⚠ Node.js not found - MCP server will not be installed${NC}"
    INSTALL_MCP=false
fi

# Create directory
echo
echo "Creating ~/.planner-cli directory..."
mkdir -p ~/.planner-cli
echo -e "${GREEN}✓ Directory created${NC}"

# Install Python dependencies
echo
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${RED}Error installing Python dependencies${NC}"
    exit 1
fi

# Copy CLI to ~/.planner-cli
echo
echo "Installing Python CLI..."
cp planner.py ~/.planner-cli/
chmod +x ~/.planner-cli/planner.py
echo -e "${GREEN}✓ CLI installed to ~/.planner-cli/planner.py${NC}"

# Create symlink (optional)
echo
read -p "Create symlink in /usr/local/bin for global access? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -w /usr/local/bin ]; then
        ln -sf ~/.planner-cli/planner.py /usr/local/bin/planner
        echo -e "${GREEN}✓ Symlink created: /usr/local/bin/planner${NC}"
    else
        sudo ln -sf ~/.planner-cli/planner.py /usr/local/bin/planner
        echo -e "${GREEN}✓ Symlink created with sudo: /usr/local/bin/planner${NC}"
    fi
fi

# Install MCP server
if [ "$INSTALL_MCP" = true ]; then
    echo
    read -p "Install MCP server? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing Node.js dependencies..."
        npm install

        echo "Building TypeScript..."
        npm run build

        if [ -f "dist/server.js" ]; then
            echo -e "${GREEN}✓ MCP server built successfully${NC}"
        else
            echo -e "${RED}Error building MCP server${NC}"
        fi
    fi
fi

# Configuration
echo
echo "=========================================="
echo "Configuration Setup"
echo "=========================================="
echo
echo "You need Azure AD credentials to use this CLI."
echo "Please have your TENANT_ID and CLIENT_ID ready."
echo
read -p "Configure now? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your TENANT_ID: " TENANT_ID
    read -p "Enter your CLIENT_ID: " CLIENT_ID

    # Create config file
    cat > ~/.planner-cli/config.json << EOF
{
  "tenant_id": "$TENANT_ID",
  "client_id": "$CLIENT_ID"
}
EOF

    chmod 600 ~/.planner-cli/config.json
    echo -e "${GREEN}✓ Configuration saved to ~/.planner-cli/config.json${NC}"

    # Test authentication
    echo
    read -p "Test authentication now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 ~/.planner-cli/planner.py init-auth
    fi
else
    echo
    echo "To configure later, create ~/.planner-cli/config.json with:"
    echo '{'
    echo '  "tenant_id": "your-tenant-id",'
    echo '  "client_id": "your-client-id"'
    echo '}'
    echo
    echo "Or set environment variables:"
    echo "export TENANT_ID=\"your-tenant-id\""
    echo "export CLIENT_ID=\"your-client-id\""
fi

# Final instructions
echo
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "1. Authenticate: planner init-auth"
echo "2. Set defaults: planner set-defaults --plan \"My Plan\" --bucket \"To Do\""
echo "3. Create a task: planner add --title \"My first task\""
echo
echo "For help: planner --help"
echo "Documentation: cat README.md"
echo
echo -e "${GREEN}Happy planning! 🚀${NC}"
