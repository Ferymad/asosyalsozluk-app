#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt

# Create necessary directories
mkdir -p temp
mkdir -p .streamlit

# Copy the Streamlit config file
cp .streamlit/config.toml.example .streamlit/config.toml

echo "Setup complete. Activate the virtual environment with 'source venv/bin/activate'"