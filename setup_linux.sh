#!/bin/bash

echo "Creating environment..."
python -m venv .venv
echo "Done"
echo "Activating environment..."
source .venv/bin/activate
echo "Done"
echo "Installing packages..."
pip install -r requirements.txt
echo "Done"