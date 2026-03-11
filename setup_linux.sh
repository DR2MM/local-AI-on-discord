#!/bin/bash

echo "Creating environment..."
python -m venv .venv
echo "Activating environment..."
source .venv/bin/activate
echo "Installing packages..."
pip install -r requirements.txt
echo "Done"
