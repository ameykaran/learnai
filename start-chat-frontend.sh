#!/bin/bash

# Start Chat Frontend

cd "$(dirname "$0")/chat_frontend"

echo "Starting Chat Frontend..."
echo "URL: http://localhost:3001"
echo ""

npm run dev
