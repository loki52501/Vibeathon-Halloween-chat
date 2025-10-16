#!/usr/bin/env python3
"""
Fix npm issues on Windows for Halloween Poe Chat
"""
import subprocess
import sys
import os
import shutil

def check_npm_installation():
    """Check if npm is properly installed and accessible"""
    print("Checking npm installation...")
    
    # Check if npm is in PATH
    npm_path = shutil.which("npm")
    if npm_path:
        print(f"SUCCESS: npm found at: {npm_path}")
        return True
    
    # Check common npm locations
    common_paths = [
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
        r"C:\Users\{}\AppData\Roaming\npm\npm.cmd".format(os.getenv('USERNAME', '')),
        r"C:\Users\{}\AppData\Local\npm\npm.cmd".format(os.getenv('USERNAME', ''))
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"SUCCESS: npm found at: {path}")
            return True
    
    print("ERROR: npm not found in common locations")
    return False

def check_node_installation():
    """Check if Node.js is properly installed"""
    print("Checking Node.js installation...")
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"SUCCESS: Node.js version: {result.stdout.strip()}")
            return True
        else:
            print("ERROR: Node.js not working properly")
            return False
    except FileNotFoundError:
        print("ERROR: Node.js not found")
        return False

def fix_npm_path():
    """Try to fix npm PATH issues"""
    print("Attempting to fix npm PATH issues...")
    
    # Common Node.js installation paths
    node_paths = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs"
    ]
    
    for path in node_paths:
        if os.path.exists(path):
            npm_path = os.path.join(path, "npm.cmd")
            if os.path.exists(npm_path):
                print(f"Found npm at: {npm_path}")
                print(f"Add this to your PATH: {path}")
                return path
    
    return None

def install_frontend_manually():
    """Install frontend dependencies manually"""
    print("Installing frontend dependencies manually...")
    
    # Try different npm commands
    npm_commands = [
        "npm install",
        "npm.cmd install",
        r"C:\Program Files\nodejs\npm.cmd install",
        r"C:\Program Files (x86)\nodejs\npm.cmd install"
    ]
    
    for cmd in npm_commands:
        try:
            print(f"Trying: {cmd}")
            result = subprocess.run(cmd, shell=True, cwd="frontend", capture_output=True, text=True)
            if result.returncode == 0:
                print("SUCCESS: Frontend dependencies installed!")
                return True
            else:
                print(f"Failed: {result.stderr}")
        except Exception as e:
            print(f"Error: {e}")
    
    return False

def main():
    print("Halloween Poe Chat - npm Fix for Windows")
    print("=" * 50)
    
    # Check Node.js
    if not check_node_installation():
        print("\nSOLUTION: Please install Node.js from https://nodejs.org/")
        print("Make sure to check 'Add to PATH' during installation")
        return False
    
    # Check npm
    if not check_npm_installation():
        print("\nTrying to fix npm PATH issues...")
        npm_path = fix_npm_path()
        if npm_path:
            print(f"\nSOLUTION: Add this to your PATH environment variable:")
            print(f"{npm_path}")
            print("\nSteps to add to PATH:")
            print("1. Press Win + R, type 'sysdm.cpl', press Enter")
            print("2. Click 'Environment Variables'")
            print("3. Under 'System Variables', find 'Path' and click 'Edit'")
            print("4. Click 'New' and add the path above")
            print("5. Click 'OK' on all dialogs")
            print("6. Restart your command prompt")
        else:
            print("\nSOLUTION: Reinstall Node.js from https://nodejs.org/")
            print("Make sure to check 'Add to PATH' during installation")
        return False
    
    # Try to install frontend dependencies
    print("\nAttempting to install frontend dependencies...")
    if install_frontend_manually():
        print("\nSUCCESS: Frontend setup completed!")
        return True
    else:
        print("\nERROR: Could not install frontend dependencies")
        print("Please fix npm PATH issues first")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\nYou can now start the frontend with:")
        print("python start_frontend.py")
    else:
        print("\nPlease fix the npm issues and try again")
