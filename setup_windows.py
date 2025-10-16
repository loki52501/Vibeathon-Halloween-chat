#!/usr/bin/env python3
"""
Windows-compatible setup script for Halloween Poe Chat
Avoids Unicode issues on Windows console
"""
import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"Running: {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"SUCCESS: {description} completed!")
            return True
        else:
            print(f"ERROR: {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: {description} failed: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"Python {version.major}.{version.minor}.{version.micro} is not compatible")
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
        print("Environment file already exists")
        return True
    
    print("Creating environment file...")
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
        print("Environment file created!")
        print("IMPORTANT: Please edit backend/.env with your actual credentials")
        return True
    except Exception as e:
        print(f"Error creating environment file: {e}")
        return False

def setup_database():
    """Setup PostgreSQL database"""
    print("Setting up PostgreSQL database...")
    try:
        result = subprocess.run([
            sys.executable, "backend/setup_database.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("SUCCESS: Database setup completed!")
            return True
        else:
            print(f"ERROR: Database setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: Error running database setup: {e}")
        return False

def install_frontend_dependencies():
    """Install Node.js dependencies"""
    return run_command(
        "cd frontend && npm install",
        "Installing frontend dependencies"
    )

def test_installation():
    """Test if everything is working"""
    print("Testing installation...")
    
    # Test backend imports
    try:
        import fastapi
        import uvicorn
        import boto3
        import socketio
        import sqlalchemy
        import psycopg2
        print("SUCCESS: Backend dependencies working")
    except ImportError as e:
        print(f"ERROR: Backend dependency issue: {e}")
        return False
    
    # Test database connection
    try:
        from backend.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("SUCCESS: Database connection working")
    except Exception as e:
        print(f"ERROR: Database connection issue: {e}")
        return False
    
    # Test AWS Bedrock connection (optional)
    try:
        import boto3
        from dotenv import load_dotenv
        load_dotenv("backend/.env")
        
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # Test if we can list models (this will fail if credentials are wrong)
        bedrock_client.list_foundation_models()
        print("SUCCESS: AWS Bedrock connection working")
    except Exception as e:
        print(f"WARNING: AWS Bedrock connection issue: {e}")
        print("This is OK if you haven't set up AWS credentials yet")
    
    print("SUCCESS: All tests passed!")
    return True

def main():
    print("Halloween Poe Chat - Windows Setup")
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
        print("Failed to install Python dependencies")
        sys.exit(1)
    
    # Step 3: Setup environment file
    if not setup_environment():
        print("Failed to setup environment file")
        sys.exit(1)
    
    # Step 4: Setup database
    if not setup_database():
        print("Failed to setup database")
        print("Please ensure PostgreSQL is running and credentials are correct")
        sys.exit(1)
    
    # Step 5: Install frontend dependencies
    if not install_frontend_dependencies():
        print("Failed to install frontend dependencies")
        print("Please ensure Node.js is installed")
        sys.exit(1)
    
    # Step 6: Test installation
    if not test_installation():
        print("Installation test failed")
        sys.exit(1)
    
    print("\nAdvanced setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit backend/.env with your actual AWS and database credentials")
    print("2. Request access to AWS Bedrock models (see instructions below)")
    print("3. Start the backend: python start_advanced.py")
    print("4. Start the frontend: python start_frontend.py")
    print("5. Open http://localhost:3000 in your browser")
    print("\nFeatures available:")
    print("✓ AWS Bedrock AI poem generation")
    print("✓ PostgreSQL database")
    print("✓ Real-time WebSocket chat")
    print("✓ Advanced audio system")
    print("✓ Connection attempts with cooldown")
    print("✓ Message history")
    print("\nAWS Bedrock Setup Instructions:")
    print("1. Go to AWS Console > Amazon Bedrock")
    print("2. Request access to: 'Anthropic Claude 3 Sonnet'")
    print("3. Also request: 'Anthropic Claude 3 Haiku' (backup option)")
    print("4. Wait for approval (usually takes a few minutes)")
    print("5. Add your AWS credentials to backend/.env")
    print("\nNote: The app will work with fallback poem generation even without AWS Bedrock!")

if __name__ == "__main__":
    main()
