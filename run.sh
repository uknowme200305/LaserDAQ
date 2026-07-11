#!/bin/bash

echo "Starting LaserDAQ..."

if [ ! -d "venv" ]; then
    echo
    echo "[ERROR] Virtual Environment not found."
    echo "Run setup.sh first."
    exit 1
fi

source venv/bin/activate

python3 main_V1B.py