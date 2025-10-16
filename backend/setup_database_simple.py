#!/usr/bin/env python3
"""
Simple database setup script for Halloween Poe Chat
Uses SQLite as fallback if PostgreSQL is not available
"""
import os
import sys
from dotenv import load_dotenv
import sqlite3
import json
import hashlib

load_dotenv()

def setup_sqlite_database():
    """Setup SQLite database as fallback"""
    print("Setting up SQLite database...")
    
    # Create database directory if it doesn't exist
    os.makedirs("backend", exist_ok=True)
    
    conn = sqlite3.connect('backend/poe_chat_simple.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            questions TEXT NOT NULL,
            answers TEXT NOT NULL,
            poem TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connection_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            target_user_id INTEGER,
            attempts INTEGER DEFAULT 0,
            last_attempt TIMESTAMP,
            cooldown_until TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (target_user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER,
            user2_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user1_id) REFERENCES users (id),
            FOREIGN KEY (user2_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            connection_id INTEGER,
            sender_id INTEGER,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (connection_id) REFERENCES connections (id),
            FOREIGN KEY (sender_id) REFERENCES users (id)
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_connection_attempts_user_target ON connection_attempts(user_id, target_user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_connections_users ON connections(user1_id, user2_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_connection_timestamp ON messages(connection_id, timestamp)')
    
    # Insert sample data
    cursor.execute("SELECT id FROM users WHERE username = ?", ("demo_user",))
    if not cursor.fetchone():
        sample_user = (
            "demo_user",
            hashlib.sha256("demo123".encode()).hexdigest(),
            json.dumps([
                "What is your favorite gothic novel?",
                "What color represents your soul?",
                "What is your spirit animal?"
            ]),
            json.dumps([
                "Dracula",
                "Deep purple",
                "Raven"
            ]),
            """In shadows deep where memories dwell,
Three secrets hidden, none can tell.
Dracula echoes through the night,
Deep purple fades into pale moonlight.

Raven speaks in hollow tones,
Through haunted halls and ancient stones.
The raven's call, the midnight chime,
These secrets lost in endless time."""
        )
        
        cursor.execute("""
            INSERT INTO users (username, password_hash, questions, answers, poem)
            VALUES (?, ?, ?, ?, ?)
        """, sample_user)
    
    conn.commit()
    conn.close()
    
    print("SQLite database setup completed successfully!")
    return True

def main():
    print("Halloween Poe Chat - Simple Database Setup")
    print("=" * 50)
    print("This will create a SQLite database for testing")
    print("(Use this if PostgreSQL is not available)")
    print()
    
    if setup_sqlite_database():
        print("\nSimple database setup completed!")
        print("You can now use the simple version:")
        print("python start_simple.py")
        return True
    else:
        print("Database setup failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
