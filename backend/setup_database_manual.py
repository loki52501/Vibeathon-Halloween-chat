#!/usr/bin/env python3
"""
Manual database setup script for Halloween Poe Chat
This script assumes the database already exists
"""
import os
import sys
from dotenv import load_dotenv
from database import create_tables, engine, SessionLocal, User
import json
import hashlib

load_dotenv()

def check_database_connection():
    """Check if we can connect to the database"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
        print("SUCCESS: Database connection successful!")
        return True
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        return False

def setup_tables():
    """Create all necessary tables"""
    try:
        print("Creating database tables...")
        create_tables()
        print("SUCCESS: All tables created successfully!")
        return True
    except Exception as e:
        print(f"ERROR: Error creating tables: {e}")
        return False

def create_indexes():
    """Create additional indexes for better performance"""
    try:
        print("Creating database indexes...")
        with engine.connect() as connection:
            # Create indexes for better performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
                "CREATE INDEX IF NOT EXISTS idx_connection_attempts_user_target ON connection_attempts(user_id, target_user_id);",
                "CREATE INDEX IF NOT EXISTS idx_connections_users ON connections(user1_id, user2_id);",
                "CREATE INDEX IF NOT EXISTS idx_messages_connection_timestamp ON messages(connection_id, timestamp);",
                "CREATE INDEX IF NOT EXISTS idx_chat_rooms_room_id ON chat_rooms(room_id);",
                "CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id);"
            ]
            
            for index_sql in indexes:
                connection.execute(index_sql)
            
            connection.commit()
            print("SUCCESS: All indexes created successfully!")
        return True
    except Exception as e:
        print(f"ERROR: Error creating indexes: {e}")
        return False

def insert_sample_data():
    """Insert some sample data for testing"""
    try:
        print("Inserting sample data...")
        
        db = SessionLocal()
        
        # Check if sample user already exists
        existing_user = db.query(User).filter(User.username == "demo_user").first()
        if existing_user:
            print("SUCCESS: Sample user already exists!")
            db.close()
            return True
        
        # Create sample user
        sample_user = User(
            username="demo_user",
            password_hash=hashlib.sha256("demo123".encode()).hexdigest(),
            questions=json.dumps([
                "What is your favorite gothic novel?",
                "What color represents your soul?",
                "What is your spirit animal?"
            ]),
            answers=json.dumps([
                "Dracula",
                "Deep purple",
                "Raven"
            ]),
            poem="""In shadows deep where memories dwell,
Three secrets hidden, none can tell.
Dracula echoes through the night,
Deep purple fades into pale moonlight.

Raven speaks in hollow tones,
Through haunted halls and ancient stones.
The raven's call, the midnight chime,
These secrets lost in endless time."""
        )
        
        db.add(sample_user)
        db.commit()
        db.close()
        
        print("SUCCESS: Sample data inserted successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: Error inserting sample data: {e}")
        return False

def main():
    print("Halloween Poe Chat - Manual Database Setup")
    print("=" * 50)
    print("This script assumes the PostgreSQL database already exists.")
    print("If you haven't created the database yet, please do so manually:")
    print("1. Connect to PostgreSQL as superuser")
    print("2. Run: CREATE DATABASE poe_chat;")
    print("3. Then run this script")
    print()
    
    # Check environment variables
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file:")
        print("DB_USER=postgres")
        print("DB_PASSWORD=your_password")
        print("DB_HOST=localhost")
        print("DB_PORT=5432")
        print("DB_NAME=poe_chat")
        return False
    
    print(f"Database URL: {os.getenv('DATABASE_URL', 'Using individual settings')}")
    print()
    
    # Step 1: Check connection
    if not check_database_connection():
        return False
    
    # Step 2: Create tables
    if not setup_tables():
        return False
    
    # Step 3: Create indexes
    if not create_indexes():
        return False
    
    # Step 4: Insert sample data
    if not insert_sample_data():
        return False
    
    print("\nDatabase setup completed successfully!")
    print("\nYou can now start the application with:")
    print("python start_advanced.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
