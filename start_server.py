#!/usr/bin/env python3
"""
Halloween Poe Chat - Main Server Startup Script
Starts the FastAPI backend with WebSocket support
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import fastapi
        import sqlalchemy
        import psycopg2
        import socketio
        import boto3
        print("✓ All Python dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r backend/requirements.txt")
        return False

def check_database():
    """Check if database is accessible"""
    try:
        from backend.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Database connection working")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("Please run: python backend/setup_database.py")
        return False

def start_server():
    """Start the main server"""
    print("🎃 Starting Halloween Poe Chat Server...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Check database
    if not check_database():
        return False
    
    print("\n🚀 Starting server on http://localhost:8000")
    print("📡 WebSocket server ready for real-time chat")
    print("🔗 API documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the server
        from backend.main_advanced import socket_app
        import uvicorn
        uvicorn.run(socket_app, host="0.0.0.0", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n👻 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = start_server()
    if not success:
        sys.exit(1)
