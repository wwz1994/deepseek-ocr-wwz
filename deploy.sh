#!/bin/bash

echo "🚀 PowerPoint Generator - Deployment Script"
echo "============================================"
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements_web.txt --user

# Test the application
echo ""
echo "🧪 Testing PowerPoint generation..."
python3 create_3d_ppt.py

# Start the server
echo ""
echo "🌐 Starting Flask server..."
echo "Server will be available at: http://0.0.0.0:5000"
echo ""
python3 app.py
