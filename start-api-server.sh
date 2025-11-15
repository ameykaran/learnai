#!/bin/bash

# Start API Server

cd "$(dirname "$0")/api_server"

echo "Starting API Server..."
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "WebSocket: ws://localhost:8000/ws/{session_id}"
echo ""

python main.py
