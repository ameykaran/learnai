#!/bin/bash

echo "🔧 Starting Adaptive Probability Quiz Backend..."

# Kill any existing processes
echo "Stopping existing backend processes..."
pkill -f "python.*main.py" 2>/dev/null || true
sleep 2

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Install dependencies if needed
echo "Installing/checking dependencies..."
python3 -m pip install fastapi uvicorn sqlalchemy pydantic python-multipart --break-system-packages --quiet

# Start the backend
echo "🚀 Starting FastAPI server on http://localhost:8000..."
python3 main.py