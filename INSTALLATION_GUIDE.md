# 🎃 Halloween Poe Chat - Installation Guide

## Quick Fix for Python 3.13 Compatibility Issues

If you're encountering pip installation errors with Python 3.13, here are several solutions:

## Option 1: Minimal Installation (Recommended for Quick Start)

Install only the essential packages:

```bash
pip install fastapi uvicorn python-dotenv
```

Then run the simplified version:

```bash
python start_simple.py
```

This version works without AWS Bedrock and uses built-in poem generation.

## Option 2: Use Python 3.11 or 3.12 (Recommended for Full Features)

If you want the full experience with AWS Bedrock integration:

1. **Install Python 3.11 or 3.12** (more stable with current packages)
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```
3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

## Option 3: Install Dependencies One by One

If you're having issues with the requirements file:

```bash
pip install fastapi
pip install uvicorn[standard]
pip install pydantic
pip install boto3
pip install python-multipart
pip install python-dotenv
pip install requests
pip install numpy
pip install python-socketio
pip install eventlet
```

## Option 4: Use Conda (Alternative Package Manager)

```bash
conda create -n poe-chat python=3.11
conda activate poe-chat
pip install -r backend/requirements.txt
```

## Frontend Setup

The frontend should work fine with Node.js:

```bash
cd frontend
npm install
npm start
```

## Testing the Application

### 1. Start Backend (Simple Version)
```bash
python start_simple.py
```

### 2. Start Frontend (in another terminal)
```bash
cd frontend
npm start
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Troubleshooting

### Common Python 3.13 Issues:

1. **Package compatibility**: Some packages may not have wheels for Python 3.13 yet
2. **Build tools**: Some packages require compilation which can fail

### Solutions:

1. **Use Python 3.11 or 3.12** (most reliable)
2. **Use the simple version** without AWS Bedrock
3. **Install packages individually** to identify problematic ones
4. **Use conda** as an alternative package manager

### If you still have issues:

1. **Check Python version:**
   ```bash
   python --version
   ```

2. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

4. **Try installing with --no-cache-dir:**
   ```bash
   pip install --no-cache-dir fastapi uvicorn python-dotenv
   ```

## Quick Demo

Once you have the simple version running, you can test it:

```bash
python demo.py
```

This will test the API endpoints and show you how the application works.

## Next Steps

1. **Get the simple version working first**
2. **Test the frontend and backend communication**
3. **If you want AWS Bedrock features, consider using Python 3.11/3.12**
4. **Set up AWS credentials in `backend/.env` for full features**

The simple version includes:
- ✅ User registration
- ✅ Poem generation (fallback)
- ✅ Connection attempts
- ✅ Cooldown system
- ✅ Basic chat functionality
- ❌ AWS Bedrock integration
- ❌ Advanced WebSocket features

This should be enough to demonstrate the core concept of the Halloween Poe Chat application!
