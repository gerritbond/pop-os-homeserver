#!/bin/bash
# Script to generate DBeaver connections CSV from PostgreSQL service .env file
# Usage: ./scripts/generate-dbeaver.sh

echo "Generating DBeaver connections from PostgreSQL service .env file..."

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root directory
cd "$PROJECT_ROOT"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Run the Python script
python "$SCRIPT_DIR/generate-dbeaver-connections.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully generated dbeaver-connections.csv"
    echo "📁 You can now import this file into DBeaver:"
    echo "   Database Navigator → Right-click → Import Connections → From CSV"
    echo ""
    echo "📋 Generated connections:"
    if [ -f dbeaver-connections.csv ]; then
        tail -n +2 dbeaver-connections.csv | cut -d',' -f1
    fi
else
    echo "❌ Failed to generate DBeaver connections"
    exit 1
fi 