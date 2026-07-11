#!/bin/bash

echo "======================================"
echo "      LaserDAQ Setup Utility"
echo "======================================"
echo

# Check Python

if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python3 not found."
    exit 1
fi

echo "[OK] Python detected."

# Create Virtual Environment

if [ ! -d "venv" ]; then
    echo "Creating Virtual Environment..."
    python3 -m venv venv
else
    echo "Virtual Environment already exists."
fi

# Activate

source venv/bin/activate

# Upgrade pip

python3 -m pip install --upgrade pip

# Install Requirements

pip install -r requirements.txt

echo
echo "======================================"
echo "LaserDAQ Setup Complete"
echo "======================================"