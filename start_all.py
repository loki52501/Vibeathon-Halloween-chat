#!/usr/bin/env python3
"""
Startup script for Halloween Poe Chat - Both Backend and Frontend
"""
import subprocess
import sys
import os
import time
import threading
import signal

def start_backend():
    """Start the backend server in a separate thread"""
    print("🚀 Starting Backend Server...")
    try:
        os.chdir("backend")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:socket_app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except Exception as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start the frontend server in a separate thread"""
    print("🚀 Starting Frontend Server...")
    try:
        os.chdir("frontend")
        subprocess.run(["npm", "start"])
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    print("🎃 Halloween Poe Chat - Full Stack Startup")
    print("=" * 50)
    print("📍 Backend: http://localhost:8000")
    print("📍 Frontend: http://localhost:3000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both servers\n")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👻 Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
