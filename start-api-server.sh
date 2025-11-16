#!/bin/bash

# Start API Server
export $(cat .env)
cd "$(dirname "$0")"

echo "Starting API Server..."
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "WebSocket: ws://localhost:8000/ws/{session_id}"
echo ""

python -m api_server.main