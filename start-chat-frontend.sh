#!/bin/bash

# Start Chat Frontend
export $(cat .env)
cd "$(dirname "$0")/chat_frontend"

echo "Starting Chat Frontend..."
echo "URL: http://localhost:3001"
echo ""

npm install
npm run dev
