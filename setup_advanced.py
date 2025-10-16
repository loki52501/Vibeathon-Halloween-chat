#!/usr/bin/env python3
"""
Complete setup script for Halloween Poe Chat Advanced Version
Handles database setup, dependency installation, and environment configuration
"""
import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please use Python 3.8 or higher")
        return False

def install_dependencies():
    """Install Python dependencies"""
    return run_command(
        "pip install -r backend/requirements.txt",
        "Installing Python dependencies"
    )

def setup_environment():
    """Setup environment file if it doesn't exist"""
    env_file = "backend/.env"
    if os.path.exists(env_file):
        print("✅ Environment file already exists")
        return True
    
    print("📝 Creating environment file...")
    env_content = """# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# PostgreSQL Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=poe_chat

# Application Settings
SECRET_KEY=your_secret_key_here
DEBUG=False
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Environment file created!")
        print("⚠️  Please edit backend/.env with your actual credentials")
        return True
    except Exception as e:
        print(f"❌ Error creating environment file: {e}")
        return False

def setup_database():
    """Setup PostgreSQL database"""
    return run_command(
        "python backend/setup_database.py",
        "Setting up PostgreSQL database"
    )

def install_frontend_dependencies():
    """Install Node.js dependencies"""
    return run_command(
        "cd frontend && npm install",
        "Installing frontend dependencies"
    )

def test_installation():
    """Test if everything is working"""
    print("🧪 Testing installation...")
    
    # Test backend imports
    try:
        import fastapi
        import uvicorn
        import boto3
        import socketio
        import sqlalchemy
        import psycopg2
        print("✅ Backend dependencies working")
    except ImportError as e:
        print(f"❌ Backend dependency issue: {e}")
        return False
    
    # Test database connection
    try:
        from backend.database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Database connection working")
    except Exception as e:
        print(f"❌ Database connection issue: {e}")
        return False
    
    print("✅ All tests passed!")
    return True

def main():
    print("🎃 Halloween Poe Chat - Advanced Setup")
    print("=" * 50)
    print("This script will set up the complete advanced version with:")
    print("• PostgreSQL database")
    print("• AWS Bedrock integration")
    print("• WebSocket real-time chat")
    print("• Advanced audio system")
    print()
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install Python dependencies
    if not install_dependencies():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Step 3: Setup environment file
    if not setup_environment():
        print("❌ Failed to setup environment file")
        sys.exit(1)
    
    # Step 4: Setup database
    if not setup_database():
        print("❌ Failed to setup database")
        print("Please ensure PostgreSQL is running and credentials are correct")
        sys.exit(1)
    
    # Step 5: Install frontend dependencies
    if not install_frontend_dependencies():
        print("❌ Failed to install frontend dependencies")
        print("Please ensure Node.js is installed")
        sys.exit(1)
    
    # Step 6: Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    print("\n🎉 Advanced setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit backend/.env with your actual AWS and database credentials")
    print("2. Start the backend: python start_advanced.py")
    print("3. Start the frontend: python start_frontend.py")
    print("4. Open http://localhost:3000 in your browser")
    print("\nFeatures available:")
    print("✅ AWS Bedrock AI poem generation")
    print("✅ PostgreSQL database")
    print("✅ Real-time WebSocket chat")
    print("✅ Advanced audio system")
    print("✅ Connection attempts with cooldown")
    print("✅ Message history")

if __name__ == "__main__":
    main()
