#!/bin/bash

echo "========================================"
echo "AI Knowledge Assistant"
echo "========================================"
echo ""
echo "Starting application..."
echo "Your API key will be loaded automatically from .env file"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "WARNING: Virtual environment not found!"
    echo "Please run quick_start.sh first"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Your API key should be in the .env file"
    echo ""
fi

echo ""
echo "Opening browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
