#!/usr/bin/env python3
"""
Script to generate DBeaver connection CSV from .env file
Usage: python generate-dbeaver-connections.py
"""

import os
import csv
import re
from pathlib import Path

def load_env_file(env_path):
    """Load environment variables from .env file"""
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars

def extract_database_configs(env_vars):
    """Extract database configurations from environment variables"""
    databases = []
    
    # Get PostgreSQL connection details
    postgres_host = env_vars.get('POSTGRES_HOST', 'localhost')
    postgres_port = env_vars.get('POSTGRES_PORT', '5432')
    
    # Process numbered database configurations (DB_1_NAME, DB_1_USER, DB_1_PASSWORD, etc.)
    counter = 1
    while True:
        db_name_key = f'DB_{counter}_NAME'
        db_user_key = f'DB_{counter}_USER'
        db_password_key = f'DB_{counter}_PASSWORD'
        
        db_name = env_vars.get(db_name_key)
        db_user = env_vars.get(db_user_key)
        db_password = env_vars.get(db_password_key)
        
        if not db_name:
            break
            
        databases.append({
            'name': db_name,
            'user': db_user,
            'password': db_password,
            'host': postgres_host,
            'port': postgres_port
        })
        counter += 1
    
    # Also check for single database configuration
    if 'DB_NAME' in env_vars and 'DB_USER' in env_vars and 'DB_PASSWORD' in env_vars:
        databases.append({
            'name': env_vars['DB_NAME'],
            'user': env_vars['DB_USER'],
            'password': env_vars['DB_PASSWORD'],
            'host': postgres_host,
            'port': postgres_port
        })
    
    return databases

def generate_dbeaver_csv(databases, output_file):
    """Generate DBeaver CSV file"""
    # DBeaver CSV format: name,driver,url,user,password
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['name', 'driver', 'url', 'user', 'password'])
        
        # Write database connections
        for db in databases:
            name = f"PostgreSQL - {db['name']}"
            driver = "org.postgresql.Driver"
            url = f"jdbc:postgresql://{db['host']}:{db['port']}/{db['name']}"
            user = db['user']
            password = db['password']
            
            writer.writerow([name, driver, url, user, password])
    
    print(f"Generated DBeaver connections CSV: {output_file}")
    print(f"Found {len(databases)} database(s):")
    for db in databases:
        print(f"  - {db['name']} (user: {db['user']})")

def main():
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Go up one level from scripts/
    env_file = project_root / '.env'
    output_file = project_root / 'dbeaver-connections.csv'
    
    print(f"Reading environment from: {env_file}")
    
    # Load environment variables
    env_vars = load_env_file(env_file)
    
    if not env_vars:
        print("No environment variables found in .env file")
        return
    
    # Extract database configurations
    databases = extract_database_configs(env_vars)
    
    if not databases:
        print("No database configurations found in .env file")
        print("Expected format:")
        print("  DB_1_NAME=database1")
        print("  DB_1_USER=user1")
        print("  DB_1_PASSWORD=password1")
        print("  DB_2_NAME=database2")
        print("  DB_2_USER=user2")
        print("  DB_2_PASSWORD=password2")
        return
    
    # Generate CSV file
    generate_dbeaver_csv(databases, output_file)

if __name__ == "__main__":
    main() 