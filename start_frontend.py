#!/usr/bin/env python3
"""
Startup script for Halloween Poe Chat Frontend
"""
import subprocess
import sys
import os
import time

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js version: {result.stdout.strip()}")
            return True
        else:
            print("✗ Node.js not found")
            return False
    except FileNotFoundError:
        print("✗ Node.js not found. Please install Node.js from https://nodejs.org/")
        return False

def check_npm():
    """Check if npm is installed"""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ npm version: {result.stdout.strip()}")
            return True
        else:
            print("✗ npm not found")
            return False
    except FileNotFoundError:
        print("✗ npm not found")
        return False

def install_dependencies():
    """Install npm dependencies"""
    print("📦 Installing frontend dependencies...")
    try:
        subprocess.run(["npm", "install"], cwd="frontend", check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def start_frontend():
    """Start the React development server"""
    print("🚀 Starting Halloween Poe Chat Frontend...")
    print("📍 Frontend will be available at: http://localhost:3000")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Change to frontend directory
        os.chdir("frontend")
        
        # Start the development server
        subprocess.run(["npm", "start"])
    except KeyboardInterrupt:
        print("\n👻 Frontend server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    print("🎃 Halloween Poe Chat Frontend Startup")
    print("=" * 40)
    
    if not check_node():
        sys.exit(1)
    
    if not check_npm():
        sys.exit(1)
    
    # Check if node_modules exists
    if not os.path.exists("frontend/node_modules"):
        if not install_dependencies():
            sys.exit(1)
    else:
        print("✓ Dependencies already installed")
    
    start_frontend()

if __name__ == "__main__":
    main()
