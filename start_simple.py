#!/usr/bin/env python3
"""
Simple startup script for Halloween Poe Chat Backend (without AWS Bedrock)
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
        import sqlite3
        print("✓ Core dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install fastapi uvicorn python-dotenv")
        return False

def start_server():
    """Start the simplified FastAPI server"""
    print("🚀 Starting Halloween Poe Chat Backend (Simple Version)...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("⚠️  Note: This version uses fallback poem generation (no AWS Bedrock)")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main_simple:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👻 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    print("🎃 Halloween Poe Chat Backend Startup (Simple Version)")
    print("=" * 50)
    
    if not check_dependencies():
        print("\nTo install minimal dependencies, run:")
        print("pip install fastapi uvicorn python-dotenv")
        sys.exit(1)
    
    start_server()

if __name__ == "__main__":
    main()
