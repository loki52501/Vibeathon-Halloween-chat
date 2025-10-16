# Windows Troubleshooting Guide

## Unicode Error Fix

The error you encountered is due to Windows console not supporting Unicode emoji characters. I've fixed this by:

1. **Removed all Unicode emojis** from the setup scripts
2. **Created Windows-compatible versions** of all scripts
3. **Added fallback options** for different setups

## Quick Solutions

### Option 1: Use the Fixed Setup Script
```bash
python setup_windows.py
```

### Option 2: Use Simple Version (No PostgreSQL Required)
```bash
# Install minimal dependencies
pip install fastapi uvicorn python-dotenv

# Setup simple SQLite database
python backend/setup_database_simple.py

# Start simple version
python start_simple.py
```

### Option 3: Manual Setup (Step by Step)

#### Step 1: Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv boto3 python-socketio
```

#### Step 2: Create Environment File
Create `backend/.env`:
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
```

#### Step 3: Setup Database
Choose one:

**For PostgreSQL (if you have it):**
```bash
# Set these in your .env file first:
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=poe_chat

python backend/setup_database.py
```

**For SQLite (simpler):**
```bash
python backend/setup_database_simple.py
```

#### Step 4: Start the Application
```bash
# For advanced version (PostgreSQL + AWS)
python start_advanced.py

# For simple version (SQLite + fallback AI)
python start_simple.py
```

## Common Issues and Solutions

### 1. Unicode/Emoji Errors
**Problem:** `UnicodeEncodeError: 'charmap' codec can't encode character`
**Solution:** Use the Windows-compatible scripts I've created

### 2. PostgreSQL Connection Issues
**Problem:** Database connection fails
**Solutions:**
- Make sure PostgreSQL is installed and running
- Check your credentials in `.env` file
- Use SQLite version instead: `python backend/setup_database_simple.py`

### 3. Missing Dependencies
**Problem:** Import errors
**Solution:** Install dependencies one by one:
```bash
pip install fastapi
pip install uvicorn
pip install python-dotenv
pip install boto3
pip install python-socketio
```

### 4. AWS Bedrock Issues
**Problem:** AWS credentials not working
**Solution:** 
- Check your AWS credentials in `.env`
- Use the simple version which has fallback poem generation

## Recommended Setup for Windows

### Minimal Setup (Recommended for Testing)
```bash
# 1. Install basic dependencies
pip install fastapi uvicorn python-dotenv

# 2. Setup simple database
python backend/setup_database_simple.py

# 3. Start simple version
python start_simple.py

# 4. In another terminal, start frontend
cd frontend
npm install
npm start
```

### Full Setup (If you have PostgreSQL)
```bash
# 1. Install all dependencies
pip install -r backend/requirements.txt

# 2. Setup environment file
# Edit backend/.env with your credentials

# 3. Setup PostgreSQL database
python backend/setup_database.py

# 4. Start advanced version
python start_advanced.py

# 5. Start frontend
cd frontend
npm install
npm start
```

## What Each Version Includes

### Simple Version (`start_simple.py`)
- ✅ User registration
- ✅ Poem generation (template-based)
- ✅ Connection attempts
- ✅ Cooldown system
- ✅ SQLite database
- ✅ Basic chat
- ❌ AWS Bedrock
- ❌ WebSocket real-time chat

### Advanced Version (`start_advanced.py`)
- ✅ Everything from simple version
- ✅ AWS Bedrock AI integration
- ✅ PostgreSQL database
- ✅ Real-time WebSocket chat
- ✅ Message history
- ✅ Advanced audio system

## Testing Your Setup

### Test Backend Only
```bash
python demo.py
```

### Test Full Application
1. Start backend: `python start_simple.py` or `python start_advanced.py`
2. Start frontend: `cd frontend && npm start`
3. Open: http://localhost:3000

## Getting Help

If you're still having issues:

1. **Try the simple version first** - it has fewer dependencies
2. **Check your Python version** - should be 3.8+
3. **Install dependencies one by one** to identify problematic packages
4. **Use SQLite instead of PostgreSQL** for easier setup

The simple version will give you a fully functional Halloween Poe Chat application without the complexity of PostgreSQL and AWS setup!
