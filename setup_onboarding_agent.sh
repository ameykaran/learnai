#!/bin/bash
# Setup script for Onboarding Agent

echo "=================================="
echo "  Onboarding Agent Setup"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

source .venv/bin/activate;
export $(cat .env)  

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
uv pip install --upgrade pip > /dev/null 2>&1
uv pip install -r requirements-agent.txt

echo ""
echo "✅ Installation complete!"
echo ""

# Check AWS credentials
echo "🔍 Checking AWS credentials..."
if aws sts get-caller-identity > /dev/null 2>&1; then
    echo "   ✅ AWS credentials configured"
    aws_region=$(aws configure get region)
    echo "   Region: $aws_region"
else
    echo "   ⚠️  AWS credentials not found"
    echo "   Please run: aws configure"
    echo "   or set environment variables:"
    echo "     export AWS_ACCESS_KEY_ID=\"...\""
    echo "     export AWS_SECRET_ACCESS_KEY=\"...\""
    echo "     export AWS_REGION=\"us-east-1\""
fi

echo ""
echo "=================================="
echo "  Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Configure AWS credentials (if not done)"
echo "2. Enable Bedrock model access in AWS console"
echo "3. Run the agent:"
echo "   python run_onboarding_agent.py --user-id test_user"
echo ""
echo "For more information, see ONBOARDING_AGENT_README.md"
echo ""
