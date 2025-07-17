#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

echo "Starting database initialization..."

# Function to create database and user
create_database_and_user() {
    local db_name="$1"
    local db_user="$2"
    local db_password="$3"
    
    if [ -n "$db_name" ] && [ -n "$db_user" ] && [ -n "$db_password" ]; then
        echo "Creating database: $db_name with user: $db_user"
        
        # Check if database exists, if not create it
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
            SELECT 'CREATE DATABASE "$db_name"' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db_name')\gexec
EOSQL
        
        # Create user if not exists
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
            DO \$\$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$db_user') THEN
                    CREATE USER "$db_user" WITH PASSWORD '$db_password';
                END IF;
            END
            \$\$;
EOSQL
        
        # Grant privileges
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
            GRANT ALL PRIVILEGES ON DATABASE "$db_name" TO "$db_user";
            ALTER USER "$db_user" CREATEDB;
EOSQL
        
        # Grant additional privileges on the new database
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$db_name" <<-EOSQL
            GRANT ALL ON SCHEMA public TO "$db_user";
            GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "$db_user";
            GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "$db_user";
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "$db_user";
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "$db_user";
EOSQL
        
        echo "Successfully created database '$db_name' and user '$db_user'"
    else
        echo "Warning: Skipping database creation - missing required environment variables"
        echo "  DB_NAME: $db_name"
        echo "  DB_USER: $db_user"
        echo "  DB_PASSWORD: [hidden]"
    fi
}

# Process numbered database configurations (DB_1_NAME, DB_1_USER, DB_1_PASSWORD, etc.)
counter=1
while true; do
    db_name_var="DB_${counter}_NAME"
    db_user_var="DB_${counter}_USER"
    db_password_var="DB_${counter}_PASSWORD"
    
    # Get the values from environment variables
    db_name="${!db_name_var}"
    db_user="${!db_user_var}"
    db_password="${!db_password_var}"
    
    # If no database name is set, we've reached the end
    if [ -z "$db_name" ]; then
        break
    fi
    
    create_database_and_user "$db_name" "$db_user" "$db_password"
    counter=$((counter + 1))
done

# Also support single database configuration (DB_NAME, DB_USER, DB_PASSWORD)
if [ -n "$DB_NAME" ] && [ -n "$DB_USER" ] && [ -n "$DB_PASSWORD" ]; then
    echo "Processing single database configuration..."
    create_database_and_user "$DB_NAME" "$DB_USER" "$DB_PASSWORD"
fi

echo "Database initialization completed!"
