# 🎃 Halloween Poe Chat - Spooky Connection App

A Halloween-themed chat application where users connect through Edgar Allan Poe-inspired poetry riddles. Enter the realm of mysterious connections where souls meet through cryptic verses and spooky encounters!

## ✨ Features

### 🔮 Core Functionality
- **Mysterious Registration**: Users create 3 personal questions/answers that define their soul
- **AI Poetry Generation**: Amazon Bedrock generates Poe-style poems from user answers
- **Riddle Solving**: Other users must decipher poems to connect (5 attempts max)
- **Connection System**: 2-minute cooldown between failed attempts
- **Real-time Chat**: WebSocket-powered chat for connected souls

### 🎵 Audio Experience
- **Dynamic Background Music**: Spooky ambient sounds using Web Audio API
- **Pitch-based Feedback**: Music pitch changes based on answer accuracy
  - High pitch (1.2x) for close answers (2+ correct)
  - Low pitch (0.8x) for wrong answers
  - Very low pitch (0.5x) during cooldown
- **Sound Effects**: Success, error, and warning sounds

### 🎨 Visual Design
- **Gothic UI**: Dark, Halloween-themed interface with glowing effects
- **Particle System**: Floating particles for atmospheric effect
- **Smooth Animations**: Framer Motion animations for transitions
- **Responsive Design**: Works on desktop and mobile devices

## 🛠 Tech Stack

- **Backend**: Python with FastAPI + SocketIO
- **Frontend**: React with Node.js
- **AI**: Amazon Bedrock (Claude) for poem generation
- **Database**: SQLite for user data and connections
- **Audio**: Web Audio API for dynamic sound generation
- **Styling**: Styled Components + CSS animations

## 📁 Project Structure

```
halloween-poe-chat/
├── backend/                 # Python FastAPI server
│   ├── main.py             # Main API server with WebSocket
│   ├── requirements.txt    # Python dependencies
│   └── env_example.txt     # Environment variables template
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Main application pages
│   │   └── App.js          # Main app component
│   ├── public/             # Static assets
│   └── package.json        # Node.js dependencies
├── knowledge_base/         # Edgar Allan Poe data
│   └── poe_poems.json      # Poems and vocabulary
├── start_backend.py        # Backend startup script
├── start_frontend.py       # Frontend startup script
├── start_all.py           # Start both servers
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- AWS Account with Bedrock access

### 1. Clone and Setup
```bash
git clone <repository-url>
cd halloween-poe-chat
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Create environment file
cp backend/env_example.txt backend/.env
# Edit backend/.env with your AWS credentials
```

### 3. Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 4. Run the Application

#### Option A: Start Both Servers
```bash
python start_all.py
```

#### Option B: Start Separately
```bash
# Terminal 1 - Backend
python start_backend.py

# Terminal 2 - Frontend  
python start_frontend.py
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration

### AWS Bedrock Setup
1. Create an AWS account
2. Enable Amazon Bedrock service
3. Request access to Claude model
4. Create IAM user with Bedrock permissions
5. Add credentials to `backend/.env`:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
```

### Environment Variables
Create `backend/.env` with:
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

## 🎮 How to Use

### 1. Registration
- Enter a mysterious username and password
- Create 3 personal questions and their answers
- The AI generates a Poe-style poem from your answers

### 2. Finding Connections
- Browse other users' poems
- Choose someone to connect with
- Attempt to solve their riddle

### 3. Solving Riddles
- Read the target user's poem carefully
- Enter your 3 answers based on the poem
- Music pitch changes based on your accuracy
- 5 attempts maximum, then 2-minute cooldown

### 4. Chatting
- Successfully connected users can chat in real-time
- Enjoy the spooky atmosphere with background music

## 🎵 Audio Features

The app uses Web Audio API to create dynamic, spooky soundscapes:

- **Background Music**: Procedurally generated ambient sounds
- **Pitch Modulation**: Music pitch changes based on user performance
- **Sound Effects**: Contextual audio feedback for actions
- **Volume Control**: Adjustable audio levels

## 🎨 Customization

### Adding New Poe Poems
Edit `knowledge_base/poe_poems.json` to add more poems and vocabulary.

### Styling Changes
Modify CSS in `frontend/src/index.css` and component styles for different themes.

### Audio Customization
Update `frontend/src/components/AudioManager.js` to change sound generation.

## 🐛 Troubleshooting

### Common Issues

1. **AWS Bedrock Access Denied**
   - Ensure Bedrock is enabled in your AWS region
   - Check IAM permissions for Bedrock access
   - Verify Claude model access

2. **Audio Not Working**
   - Check browser audio permissions
   - Ensure Web Audio API is supported
   - Try refreshing the page

3. **Connection Issues**
   - Verify both servers are running
   - Check firewall settings
   - Ensure ports 3000 and 8000 are available

### Debug Mode
Enable debug logging by setting environment variables:
```bash
export DEBUG=1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎃 Happy Halloween!

Enter the shadows, solve the riddles, and connect with souls through the mysterious poetry of Edgar Allan Poe. May your journey through the dark realm be filled with spooky encounters and gothic connections!

---

*"Once upon a midnight dreary, while I pondered, weak and weary..."* - Edgar Allan Poe
