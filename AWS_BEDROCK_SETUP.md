# AWS Bedrock Setup Guide for Halloween Poe Chat

## 🤖 Which Models to Request Access For

### **Primary Model (Recommended):**
- **Anthropic Claude 3 Sonnet** (`anthropic.claude-3-sonnet-20240229-v1:0`)
  - Best for creative writing and poetry generation
  - High quality output
  - Good balance of speed and quality

### **Backup Models (Optional):**
- **Anthropic Claude 3 Haiku** (`anthropic.claude-3-haiku-20240307-v1:0`)
  - Faster and cheaper
  - Good for simple tasks
- **Anthropic Claude 2** (`anthropic.claude-v2`)
  - Older but reliable model
  - Used as fallback in the code

## 🚀 Step-by-Step Setup

### 1. AWS Account Setup
1. **Create AWS Account** (if you don't have one)
2. **Sign in to AWS Console**
3. **Navigate to Amazon Bedrock**

### 2. Request Model Access
1. **Go to AWS Console > Amazon Bedrock**
2. **Click "Model access" in the left sidebar**
3. **Click "Request model access"**
4. **Select the following models:**
   - ✅ Anthropic Claude 3 Sonnet
   - ✅ Anthropic Claude 3 Haiku (optional)
   - ✅ Anthropic Claude 2 (optional)

### 3. Wait for Approval
- **Approval time:** Usually 5-15 minutes
- **You'll receive an email** when access is granted
- **Check the Model access page** to confirm

### 4. Configure Your Application
1. **Get your AWS credentials:**
   - Go to AWS Console > IAM
   - Create a new user or use existing
   - Attach policy: `AmazonBedrockFullAccess`
   - Create access keys

2. **Update your `.env` file:**
   ```env
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   ```

### 5. Test the Setup
```bash
# Test if Bedrock is working
python -c "
import boto3
from dotenv import load_dotenv
import os

load_dotenv('backend/.env')
client = boto3.client('bedrock-runtime', 
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
print('SUCCESS: AWS Bedrock connection working!')
"
```

## 🔧 Model Configuration in Code

The application is configured to use these models in order of preference:

1. **Claude 3 Sonnet** (primary)
2. **Claude 2** (fallback)
3. **Template-based generation** (if AWS fails)

### Code Location:
- **File:** `backend/main_advanced.py`
- **Function:** `generate_poe_poem()`
- **Model ID:** `anthropic.claude-v2` (can be updated to Claude 3)

## 💰 Cost Information

### **Claude 3 Sonnet:**
- **Input:** $3.00 per 1M tokens
- **Output:** $15.00 per 1M tokens
- **Typical poem cost:** ~$0.001-0.005 per poem

### **Claude 3 Haiku:**
- **Input:** $0.25 per 1M tokens
- **Output:** $1.25 per 1M tokens
- **Typical poem cost:** ~$0.0001-0.0005 per poem

### **Claude 2:**
- **Input:** $8.00 per 1M tokens
- **Output:** $24.00 per 1M tokens
- **Typical poem cost:** ~$0.002-0.01 per poem

## 🛠️ Troubleshooting

### Common Issues:

#### 1. "Access Denied" Error
- **Cause:** Model access not approved yet
- **Solution:** Wait for approval or check Model access page

#### 2. "Invalid credentials" Error
- **Cause:** Wrong AWS credentials
- **Solution:** Check your `.env` file and IAM permissions

#### 3. "Region not supported" Error
- **Cause:** Bedrock not available in your region
- **Solution:** Use `us-east-1` or `us-west-2`

#### 4. "Model not found" Error
- **Cause:** Model ID is incorrect
- **Solution:** Check the exact model ID in Bedrock console

### Fallback Options:
If AWS Bedrock doesn't work, the application will:
1. **Use template-based poem generation**
2. **Still provide full functionality**
3. **Work without AI features**

## 🎯 Quick Start (Without AWS)

If you want to test the application without AWS Bedrock:

1. **Skip AWS setup**
2. **Use the simple version:**
   ```bash
   python backend/setup_database_simple.py
   python start_simple.py
   ```
3. **The app will use template-based poems**

## 📝 Example .env Configuration

```env
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# PostgreSQL Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=poe_chat

# Application Settings
SECRET_KEY=your_secret_key_here
DEBUG=False
```

## 🎉 Success!

Once everything is set up, you'll have:
- ✅ AI-powered Poe-style poem generation
- ✅ Cryptic message generation
- ✅ Fallback to template-based generation
- ✅ Full Halloween Poe Chat functionality

The application will automatically detect if AWS Bedrock is available and use it, or fall back to template-based generation if not.
