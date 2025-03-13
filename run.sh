#!/bin/bash

# Check if .env file exists
if [ -f .env ]; then
    # Load environment variables from .env file
    export $(cat .env | grep -v '^#' | xargs)

    # Run the Python script
    python3 deep_research_agent.py
else
    echo "Error: .env file not found"
    exit 1
fi
