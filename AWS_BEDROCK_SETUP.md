# AWS Bedrock Setup Guide

## 🎯 Quick Setup

### 1. Create AWS Account
- Go to [AWS Console](https://aws.amazon.com/console/)
- Sign up for a free account (if you don't have one)

### 2. Request Model Access
- Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
- Click "Model access" in the left sidebar
- Request access to these models:
  - ✅ **Anthropic Claude 3 Sonnet** (recommended)
  - ✅ **Anthropic Claude 3 Haiku** (backup option)
  - ✅ **Anthropic Claude 2** (backup option)

### 3. Create IAM User
- Go to [IAM Console](https://console.aws.amazon.com/iam/)
- Click "Users" → "Create user"
- Username: `poe-chat-bedrock`
- Attach policy: `AmazonBedrockFullAccess`
- Create access key (save the credentials!)

### 4. Configure Environment
Create `backend/.env` file:
```env
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1

# PostgreSQL Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=poe_chat
```

### 5. Test Configuration
```bash
python test_bedrock.py
```

## 🔧 Troubleshooting

### Model Access Denied
- Wait 5-10 minutes after requesting access
- Check if your AWS account is verified
- Try different regions (us-west-2, eu-west-1)

### Credentials Error
- Make sure `.env` file is in `backend/` folder
- Check that credentials don't have extra spaces
- Verify IAM user has Bedrock permissions

### No Response from Models
- Check AWS Bedrock console for usage limits
- Try different Claude models
- Check your AWS billing (free tier limits)

## 🎭 What You'll Get

With AWS Bedrock working, you'll get:
- **AI-generated Poe-style poems** from your personal answers
- **Cryptic messages** that transform your answers into gothic riddles
- **Dynamic content** that's unique every time
- **Professional quality** AI-generated text

## 💰 Cost Information

- **Claude 3 Sonnet**: ~$0.003 per 1K tokens
- **Claude 3 Haiku**: ~$0.00025 per 1K tokens
- **Typical poem**: ~500 tokens = $0.0015
- **Free tier**: 1,000 requests/month

## 🚀 Alternative: Enhanced Fallback

If you can't set up AWS Bedrock, the app will use enhanced fallback templates that still provide:
- Gothic, Poe-style language
- Integration of your personal answers
- Mysterious and atmospheric content
- Multiple template variations

The fallback is quite good, but the AI version is much more dynamic and creative!