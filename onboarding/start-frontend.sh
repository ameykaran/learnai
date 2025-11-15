#!/bin/bash

echo "🔧 Starting Adaptive Probability Quiz Frontend..."

# Kill any existing processes
echo "Stopping existing frontend processes..."
pkill -f "npm.*dev" 2>/dev/null || true
pkill -f "next" 2>/dev/null || true
sleep 2

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Clean cache and install dependencies
echo "Cleaning Next.js cache..."
rm -rf .next
echo "Installing/checking dependencies..."
npm install --silent

# Start the frontend
echo "🚀 Starting Next.js development server..."
npm run dev