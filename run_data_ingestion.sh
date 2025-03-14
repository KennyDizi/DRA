#!/bin/bash

# Initialize default collection name
COLLECTION_NAME=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --collection-name)
            if [[ -z "$2" || "$2" == -* ]]; then
                echo "Error: --collection-name requires a value"
                exit 1
            fi
            COLLECTION_NAME="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Execute Python command with proper arguments
PYTHON_CMD="from data_ingestion_agent import DataIngestionAgent; DataIngestionAgent("
if [[ -n "$COLLECTION_NAME" ]]; then
    PYTHON_CMD+="knowledge_base_collection='$COLLECTION_NAME'"
fi
PYTHON_CMD+=").ingest_data()"

python3 -c "$PYTHON_CMD"
