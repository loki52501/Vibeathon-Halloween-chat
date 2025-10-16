# 🎃 Halloween Poe Chat - Advanced Setup Guide

## 🚀 Complete Advanced Setup with PostgreSQL & AWS Bedrock

This guide will help you set up the full-featured version with:
- ✅ PostgreSQL database
- ✅ AWS Bedrock AI integration
- ✅ Real-time WebSocket chat
- ✅ Advanced audio system
- ✅ Message history
- ✅ Connection management

## 📋 Prerequisites

### 1. Software Requirements
- **Python 3.8+** (recommended: Python 3.11 or 3.12)
- **Node.js 16+**
- **PostgreSQL 12+**
- **AWS Account** with Bedrock access

### 2. AWS Setup
1. Create an AWS account
2. Enable Amazon Bedrock service
3. Request access to Claude model
4. Create IAM user with Bedrock permissions
5. Get your AWS credentials

### 3. PostgreSQL Setup
1. Install PostgreSQL
2. Create a database user
3. Create a database for the application

## 🛠 Quick Setup (Automated)

### Option 1: Automated Setup Script
```bash
python setup_advanced.py
```

This script will:
- Install all dependencies
- Create environment file
- Setup database
- Test the installation

### Option 2: Manual Setup

#### Step 1: Install Dependencies
```bash
pip install -r backend/requirements.txt
cd frontend && npm install
```

#### Step 2: Configure Environment
Create `backend/.env`:
```env
# AWS Bedrock Configuration
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
```

#### Step 3: Setup Database
```bash
python backend/setup_database.py
```

#### Step 4: Start the Application
```bash
# Terminal 1 - Backend
python start_advanced.py

# Terminal 2 - Frontend
python start_frontend.py
```

## 🗄️ Database Schema

The application creates these tables:

### Users Table
- `id` - Primary key
- `username` - Unique username
- `password_hash` - Hashed password
- `questions` - JSON array of user questions
- `answers` - JSON array of user answers
- `poem` - Generated Poe-style poem
- `created_at` - Registration timestamp

### Connection Attempts Table
- `id` - Primary key
- `user_id` - User making attempt
- `target_user_id` - Target user
- `attempts` - Number of attempts
- `last_attempt` - Last attempt timestamp
- `cooldown_until` - Cooldown expiration

### Connections Table
- `id` - Primary key
- `user1_id` - First user
- `user2_id` - Second user
- `created_at` - Connection timestamp
- `is_active` - Connection status

### Messages Table
- `id` - Primary key
- `connection_id` - Associated connection
- `sender_id` - Message sender
- `content` - Message content
- `timestamp` - Message timestamp
- `is_read` - Read status

### Chat Rooms Table
- `id` - Primary key
- `room_id` - Unique room identifier
- `user1_id` - First user
- `user2_id` - Second user
- `created_at` - Room creation timestamp
- `is_active` - Room status

## 🔧 Advanced Features

### 1. AWS Bedrock Integration
- **Poem Generation**: Uses Claude to create Poe-style poems
- **Cryptic Messages**: Generates mysterious feedback messages
- **Fallback System**: Works without AWS if needed

### 2. Real-time WebSocket Chat
- **Live Messaging**: Instant message delivery
- **User Presence**: Shows when users join/leave
- **Room Management**: Automatic room creation
- **Message History**: Persistent message storage

### 3. Advanced Audio System
- **Dynamic Music**: Pitch changes based on performance
- **Sound Effects**: Contextual audio feedback
- **Volume Control**: Adjustable audio levels
- **Procedural Generation**: Unique ambient sounds

### 4. Connection Management
- **Attempt Tracking**: Monitors connection attempts
- **Cooldown System**: Prevents spam attempts
- **Success Detection**: Automatic connection creation
- **History Tracking**: Persistent attempt records

## 🎮 Usage Guide

### 1. User Registration
1. Enter username and password
2. Create 3 personal questions and answers
3. AI generates a Poe-style poem from your answers

### 2. Finding Connections
1. Browse other users' poems
2. Choose someone to connect with
3. Attempt to solve their riddle

### 3. Solving Riddles
1. Read the target user's poem carefully
2. Enter your 3 answers based on the poem
3. Music pitch changes based on accuracy
4. 5 attempts maximum, then 2-minute cooldown

### 4. Real-time Chat
1. Successfully connected users can chat
2. Messages are delivered instantly via WebSocket
3. Message history is preserved in database
4. Enjoy the spooky atmosphere with background music

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U postgres -d poe_chat
```

#### 2. AWS Bedrock Access Issues
- Ensure Bedrock is enabled in your AWS region
- Check IAM permissions for Bedrock access
- Verify Claude model access

#### 3. WebSocket Connection Issues
- Check firewall settings
- Ensure ports 3000 and 8000 are available
- Verify CORS settings

#### 4. Audio Issues
- Check browser audio permissions
- Ensure Web Audio API is supported
- Try refreshing the page

### Debug Mode
Enable debug logging:
```bash
export DEBUG=1
python start_advanced.py
```

## 📊 Performance Optimization

### Database Optimization
- Indexes are automatically created for better performance
- Connection pooling is configured
- Query optimization for large datasets

### WebSocket Optimization
- Efficient room management
- Connection cleanup on disconnect
- Message batching for high traffic

### Audio Optimization
- Efficient oscillator management
- Memory cleanup for audio resources
- Adaptive quality based on performance

## 🔒 Security Features

### Authentication
- Password hashing with SHA-256
- Session management
- User validation

### Data Protection
- SQL injection prevention
- XSS protection
- CORS configuration

### Rate Limiting
- Connection attempt limits
- Cooldown periods
- Spam prevention

## 📈 Monitoring & Logging

### Application Logs
- WebSocket connection logs
- Database operation logs
- Error tracking

### Performance Metrics
- Connection attempt success rates
- Message delivery times
- Audio system performance

## 🚀 Deployment

### Production Setup
1. Use production PostgreSQL instance
2. Configure AWS credentials securely
3. Set up reverse proxy (nginx)
4. Enable SSL/TLS
5. Configure monitoring

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🎉 Success!

Once everything is set up, you'll have a fully functional Halloween Poe Chat application with:

- ✅ AI-powered poem generation
- ✅ Real-time chat functionality
- ✅ Advanced audio system
- ✅ Persistent data storage
- ✅ Connection management
- ✅ Spooky Halloween theme

Access your application at: http://localhost:3000

---

*"Once upon a midnight dreary, while I pondered, weak and weary..."* - Edgar Allan Poe
