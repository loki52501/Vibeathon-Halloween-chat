#!/usr/bin/env python3
"""
Advanced startup script for Halloween Poe Chat Backend
Includes PostgreSQL, WebSocket, and AWS Bedrock integration
"""
import subprocess
import sys
import os
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import boto3
        import socketio
        import sqlalchemy
        import psycopg2
        print("✓ All advanced dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r backend/requirements.txt")
        return False

def check_env_file():
    """Check if environment file exists and has required variables"""
    env_file = "backend/.env"
    if not os.path.exists(env_file):
        print("⚠ Warning: .env file not found")
        print("Please create backend/.env with your credentials:")
        print("AWS_REGION=us-east-1")
        print("AWS_ACCESS_KEY_ID=your_access_key_here")
        print("AWS_SECRET_ACCESS_KEY=your_secret_key_here")
        print("DB_USER=postgres")
        print("DB_PASSWORD=your_password")
        print("DB_HOST=localhost")
        print("DB_PORT=5432")
        print("DB_NAME=poe_chat")
        return False
    
    # Check for required environment variables
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    required_vars = [
        'AWS_REGION', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
        'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print("⚠ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✓ Environment file and variables found")
    return True

def setup_database():
    """Run database setup"""
    print("🔧 Setting up database...")
    try:
        result = subprocess.run([
            sys.executable, "backend/setup_database.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database setup completed successfully!")
            return True
        else:
            print(f"❌ Database setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running database setup: {e}")
        return False

def start_server():
    """Start the advanced FastAPI server"""
    print("🚀 Starting Halloween Poe Chat Backend (Advanced Version)...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/socket.io/")
    print("🤖 AWS Bedrock integration: ENABLED")
    print("🗄️  Database: PostgreSQL")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main_advanced:socket_app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👻 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    print("Halloween Poe Chat Backend Startup (Advanced Version)")
    print("=" * 60)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_env_file():
        print("\nPlease set up your .env file before continuing.")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("\nDatabase setup failed. Please check your PostgreSQL connection.")
        sys.exit(1)
    
    start_server()

if __name__ == "__main__":
    main()
