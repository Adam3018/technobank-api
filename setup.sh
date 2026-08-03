#!/bin/bash
# FastAPI CRUD Application Setup Script for macOS/Linux

echo ""
echo "========================================"
echo "FastAPI CRUD Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Python is installed. Creating virtual environment..."

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo "  3. Open browser: http://localhost:8000/docs"
echo ""
