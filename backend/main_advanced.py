from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
import boto3
import json
import hashlib
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import socketio
from database import get_db, User, ConnectionAttempt, Connection, Message, ChatRoom, create_tables

load_dotenv()

app = FastAPI(title="Halloween Poe Chat API - Advanced", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Bedrock client
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Create SocketIO server for real-time chat
sio = socketio.AsyncServer(
    cors_allowed_origins=["http://localhost:3000"],
    logger=True,
    engineio_logger=True
)

# Store active connections
active_connections: Dict[str, set] = {}
user_rooms: Dict[str, str] = {}

# Pydantic models
class UserRegistration(BaseModel):
    username: str
    password: str
    questions: List[str]
    answers: List[str]

class ConnectionAttempt(BaseModel):
    target_username: str
    answers: List[str]

class MessageData(BaseModel):
    content: str
    target_username: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_poe_poem(answers: List[str]) -> str:
    """Generate a Poe-style poem from user answers using Bedrock"""
    try:
        prompt = f"""
        You are Edgar Allan Poe. Create a dark, mysterious poem that cryptically references these three personal details:
        1. {answers[0] if len(answers) > 0 else 'Unknown'}
        2. {answers[1] if len(answers) > 1 else 'Unknown'}
        3. {answers[2] if len(answers) > 2 else 'Unknown'}
        
        The poem should be in Poe's style - dark, gothic, with themes of mystery, death, and the supernatural.
        Make it cryptic so that someone familiar with these details could recognize them, but others would find it mysterious.
        Use 4-6 stanzas with 4 lines each. Include gothic imagery and Poe's characteristic rhythm.
        """
        
        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.8
        })
        
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-v2',
            body=body,
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        return response_body.get('completion', 'Failed to generate poem')
        
    except Exception as e:
        # Fallback poem if Bedrock fails
        return f"""
        In shadows deep where memories dwell,
        Three secrets hidden, none can tell.
        {answers[0] if len(answers) > 0 else 'Whispers'} echo through the night,
        {answers[1] if len(answers) > 1 else 'Dreams'} fade into pale moonlight.
        
        {answers[2] if len(answers) > 2 else 'Silence'} speaks in hollow tones,
        Through haunted halls and ancient stones.
        The raven's call, the midnight chime,
        These secrets lost in endless time.
        """

def generate_cryptic_message(answers: List[str]) -> str:
    """Generate a cryptic message from answers using Bedrock"""
    try:
        prompt = f"""
        You are Edgar Allan Poe. Transform these personal details into a cryptic, scary message:
        {', '.join(answers)}
        
        Make it sound like a mysterious riddle or warning from beyond the grave.
        Use gothic language and Poe's characteristic dark imagery.
        Keep it under 100 words but make it haunting and memorable.
        """
        
        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.9
        })
        
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-v2',
            body=body,
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        return response_body.get('completion', 'The spirits whisper in the darkness...')
        
    except Exception as e:
        return f"Beware, mortal! The answers you seek lie hidden in the shadows of {', '.join(answers[:2])}..."

# SocketIO Events
@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    # Clean up user connections
    for username, rooms in active_connections.items():
        if sid in rooms:
            rooms.remove(sid)
            if not rooms:
                del active_connections[username]
            break

@sio.event
async def join_chat(sid, data):
    """Handle user joining a chat room"""
    username = data.get('username')
    target_username = data.get('targetUsername')
    
    if not username or not target_username:
        return
    
    # Create room ID for the chat
    room_id = f"chat_{min(username, target_username)}_{max(username, target_username)}"
    
    # Join the room
    await sio.enter_room(sid, room_id)
    
    # Store connection info
    if username not in active_connections:
        active_connections[username] = set()
    active_connections[username].add(sid)
    user_rooms[username] = room_id
    
    # Notify others in the room
    await sio.emit('user_joined', {
        'username': username,
        'timestamp': datetime.now().isoformat()
    }, room=room_id, skip_sid=sid)

@sio.event
async def message(sid, data):
    """Handle incoming messages"""
    username = data.get('sender')
    target_username = data.get('targetUsername')
    message_text = data.get('text')
    
    if not username or not target_username or not message_text:
        return
    
    # Create room ID
    room_id = f"chat_{min(username, target_username)}_{max(username, target_username)}"
    
    # Prepare message data
    message_data = {
        'id': data.get('id'),
        'text': message_text,
        'sender': username,
        'timestamp': data.get('timestamp'),
        'room_id': room_id
    }
    
    # Send message to all users in the room
    await sio.emit('message', message_data, room=room_id)

@sio.event
async def leave_chat(sid, data):
    """Handle user leaving a chat room"""
    username = data.get('username')
    
    if username in user_rooms:
        room_id = user_rooms[username]
        
        # Leave the room
        await sio.leave_room(sid, room_id)
        
        # Notify others in the room
        await sio.emit('user_left', {
            'username': username,
            'timestamp': datetime.now().isoformat()
        }, room=room_id, skip_sid=sid)
        
        # Clean up
        if username in active_connections:
            active_connections[username].discard(sid)
            if not active_connections[username]:
                del active_connections[username]
        
        if username in user_rooms:
            del user_rooms[username]

# API Endpoints
@app.post("/register")
async def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    """Register a new user with their questions and answers"""
    try:
        # Check if username exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Generate poem from answers
        poem = generate_poe_poem(user_data.answers)
        
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Create user
        user = User(
            username=user_data.username,
            password_hash=password_hash,
            questions=json.dumps(user_data.questions),
            answers=json.dumps(user_data.answers),
            poem=poem
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            "message": "User registered successfully",
            "user_id": user.id,
            "poem": poem
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    """Get list of all users (for connection attempts)"""
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username, "poem": user.poem} for user in users]

@app.post("/attempt-connection")
async def attempt_connection(attempt: ConnectionAttempt, db: Session = Depends(get_db)):
    """Attempt to connect to another user by answering their questions"""
    try:
        # Get target user
        target_user = db.query(User).filter(User.username == attempt.target_username).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check cooldown
        attempt_record = db.query(ConnectionAttempt).filter(
            ConnectionAttempt.user_id == 1,  # Assuming user_id = 1 for now
            ConnectionAttempt.target_user_id == target_user.id
        ).first()
        
        if attempt_record:
            if attempt_record.cooldown_until and attempt_record.cooldown_until > datetime.now():
                remaining_time = attempt_record.cooldown_until - datetime.now()
                raise HTTPException(
                    status_code=429, 
                    detail=f"Cooldown active. Try again in {remaining_time.seconds} seconds"
                )
            
            if attempt_record.attempts >= 5:
                # Set 2-minute cooldown
                attempt_record.cooldown_until = datetime.now() + timedelta(minutes=2)
                attempt_record.attempts = 0
                db.commit()
                raise HTTPException(status_code=429, detail="Too many attempts. 2-minute cooldown activated.")
        
        # Check answers
        target_answers = json.loads(target_user.answers)
        correct_answers = 0
        for i, answer in enumerate(attempt.answers):
            if i < len(target_answers) and answer.lower().strip() == target_answers[i].lower().strip():
                correct_answers += 1
        
        # Update attempt record
        if attempt_record:
            attempt_record.attempts += 1
            attempt_record.last_attempt = datetime.now()
        else:
            attempt_record = ConnectionAttempt(
                user_id=1,  # Assuming user_id = 1 for now
                target_user_id=target_user.id,
                attempts=1,
                last_attempt=datetime.now()
            )
            db.add(attempt_record)
        
        db.commit()
        
        # Generate cryptic message
        cryptic_message = generate_cryptic_message(attempt.answers)
        
        if correct_answers == 3:
            # All answers correct - create connection
            connection = Connection(user1_id=1, user2_id=target_user.id)  # Assuming user_id = 1
            db.add(connection)
            db.commit()
            
            return {
                "success": True,
                "message": "Connection successful! You can now chat.",
                "cryptic_message": cryptic_message,
                "correct_answers": correct_answers
            }
        else:
            return {
                "success": False,
                "message": f"Only {correct_answers}/3 answers correct. Try again.",
                "cryptic_message": cryptic_message,
                "correct_answers": correct_answers,
                "pitch_level": "high" if correct_answers >= 2 else "low"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/connections/{user_id}")
async def get_connections(user_id: int, db: Session = Depends(get_db)):
    """Get user's connections"""
    connections = db.query(Connection).filter(
        (Connection.user1_id == user_id) | (Connection.user2_id == user_id)
    ).all()
    
    connected_users = []
    for conn in connections:
        other_user_id = conn.user2_id if conn.user1_id == user_id else conn.user1_id
        other_user = db.query(User).filter(User.id == other_user_id).first()
        if other_user:
            connected_users.append({"username": other_user.username})
    
    return connected_users

@app.get("/messages/{user_id}/{target_username}")
async def get_messages(user_id: int, target_username: str, db: Session = Depends(get_db)):
    """Get messages between two users"""
    target_user = db.query(User).filter(User.username == target_username).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    connection = db.query(Connection).filter(
        ((Connection.user1_id == user_id) & (Connection.user2_id == target_user.id)) |
        ((Connection.user1_id == target_user.id) & (Connection.user2_id == user_id))
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="No connection found")
    
    messages = db.query(Message).filter(Message.connection_id == connection.id).order_by(Message.timestamp).all()
    
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.username,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]

# Mount SocketIO on FastAPI
socket_app = socketio.ASGIApp(sio, app)

if __name__ == "__main__":
    import uvicorn
    # Create tables if they don't exist
    create_tables()
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
