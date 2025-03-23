#!/bin/bash
set -euo pipefail

echo "Starting linting process..."

find . -type f -name "*.py" -print0 | while IFS= read -r -d '' file; do
    echo "Running: ruff check \"$file\" --fix"
    ruff check "$file" --fix
done

echo "Linting complete!"
