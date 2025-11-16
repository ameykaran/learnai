#!/bin/bash

# Setup script for Chat Interface

set -e

echo "======================================================================"
echo "  Chat Interface Setup"
echo "======================================================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

echo -e "${YELLOW}Project root: ${PROJECT_ROOT}${NC}"

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo ""
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3${NC}"

if ! command_exists node; then
    echo -e "${RED}✗ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js${NC}"

if ! command_exists pnpm; then
    echo -e "${RED}✗ pnpm is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pnpm${NC}"

# Check AWS credentials
echo ""
echo "Checking AWS credentials..."
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo -e "${YELLOW}⚠ AWS credentials not set in environment${NC}"
    echo "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
else
    echo -e "${GREEN}✓ AWS credentials set${NC}"
fi

# Setup API Server
echo ""
echo "======================================================================"
echo "  Setting up API Server"
echo "======================================================================"

cd "$PROJECT_ROOT/api_server"

echo "Installing Python dependencies..."
uv pip install -r requirements.txt

echo -e "${GREEN}✓ API server setup complete${NC}"

# Setup Frontend
echo ""
echo "======================================================================"
echo "  Setting up Chat Frontend"
echo "======================================================================"

cd "$PROJECT_ROOT/chat_frontend"

echo "Installing Node.js dependencies..."
pnpm install

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.local.example .env.local
    echo -e "${GREEN}✓ Created .env.local${NC}"
else
    echo -e "${YELLOW}⚠ .env.local already exists${NC}"
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Final instructions
echo ""
echo "======================================================================"
echo "  Setup Complete!"
echo "======================================================================"
echo ""
echo "To start the system:"
echo ""
echo "  1. Start API Server (Terminal 1):"
echo "     cd $PROJECT_ROOT/api_server"
echo "     python main.py"
echo ""
echo "  2. Start Frontend (Terminal 2):"
echo "     cd $PROJECT_ROOT/chat_frontend"
echo "     pnpm run dev"
echo ""
echo "Then open: http://localhost:3001"
echo ""
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "======================================================================"
