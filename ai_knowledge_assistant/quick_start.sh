#!/bin/bash

echo "========================================"
echo "AI Knowledge Assistant - Quick Start"
echo "========================================"
echo ""

echo "[1/4] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed or not in PATH"
    exit 1
fi
echo ""

echo "[2/4] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi
echo ""

echo "[3/4] Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo ""

echo "[4/4] Running setup verification..."
python test_setup.py
echo ""

echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: streamlit run app.py"
echo ""
