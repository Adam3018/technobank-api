#!/bin/bash
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Install Python 3.8+ first."
    exit 1
fi

[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "Setup complete. To run:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
