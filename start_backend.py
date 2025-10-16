#!/usr/bin/env python3
"""
Startup script for Halloween Poe Chat Backend
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
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r backend/requirements.txt")
        return False

def check_env_file():
    """Check if environment file exists"""
    env_file = "backend/.env"
    if not os.path.exists(env_file):
        print("⚠ Warning: .env file not found")
        print("Please create backend/.env with your AWS credentials:")
        print("AWS_REGION=us-east-1")
        print("AWS_ACCESS_KEY_ID=your_access_key_here")
        print("AWS_SECRET_ACCESS_KEY=your_secret_key_here")
        return False
    print("✓ Environment file found")
    return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Halloween Poe Chat Backend...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/socket.io/")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:socket_app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👻 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    print("🎃 Halloween Poe Chat Backend Startup")
    print("=" * 40)
    
    if not check_dependencies():
        sys.exit(1)
    
    check_env_file()
    
    start_server()

if __name__ == "__main__":
    main()
