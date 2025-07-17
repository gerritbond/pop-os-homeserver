# Scripts Directory

This directory contains utility scripts for the popos-homeserver project.

## DBeaver Connection Generator

### Files:
- `generate-dbeaver-connections.py` - Main Python script
- `generate-dbeaver.sh` - Shell script wrapper

### Usage:

#### Option 1: Shell Script (Recommended)
```bash
./scripts/generate-dbeaver.sh
```

#### Option 2: Python Script Directly
```bash
python scripts/generate-dbeaver-connections.py
```

### What it does:
1. Reads the `.env` file from the project root
2. Extracts database configurations (DB_1_NAME, DB_1_USER, DB_1_PASSWORD, etc.)
3. Generates a `dbeaver-connections.csv` file in the project root
4. The CSV file can be imported into DBeaver for easy database connections

### Requirements:
- Python 3.x
- `.env` file with database configurations

### Output:
- Creates `dbeaver-connections.csv` in the project root
- File is automatically added to `.gitignore` to prevent committing sensitive data

### DBeaver Import Instructions:
1. Run the script: `./scripts/generate-dbeaver.sh`
2. Open DBeaver
3. Right-click in Database Navigator
4. Select "Import Connections" → "From CSV"
5. Choose the generated `dbeaver-connections.csv` file 