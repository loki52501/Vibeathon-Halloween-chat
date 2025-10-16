#!/usr/bin/env python3
"""
Halloween Poe Chat - Simple Startup Script
"""
import subprocess
import sys
import os
import time
import threading

def start_backend():
    """Start the FastAPI backend server"""
    print("🔮 Starting Backend Server...")
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start the React frontend server"""
    print("🎭 Starting Frontend Server...")
    try:
        os.chdir("frontend")
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    """Main function to start both servers"""
    print("🎃 Welcome to Halloween Poe Chat! 🎃")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Please run this script from the project root directory")
        print("   Make sure you have 'backend' and 'frontend' folders")
        return
    
    print("🚀 Starting both servers...")
    print("   Backend: http://localhost:8000")
    print("   Frontend: http://localhost:3000")
    print("   Press Ctrl+C to stop both servers")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("👻 Goodbye! Thanks for using Halloween Poe Chat!")

if __name__ == "__main__":
    main()
