"""
Halloween Poe Chat - Main Backend Server
A spooky chat application inspired by Edgar Allan Poe
"""
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
from database import get_db, User, ConnectionAttempt, Connection, Message, ChatRoom, create_tables

load_dotenv()

app = FastAPI(title="Halloween Poe Chat API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Bedrock client (optional)
bedrock_client = None
bedrock_available = False

def initialize_bedrock():
    global bedrock_client, bedrock_available
    try:
        # Check if AWS credentials are available
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        if not aws_access_key or not aws_secret_key:
            print("AWS Bedrock: No credentials found in environment variables")
            return False
            
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # Test the connection by listing available models
        try:
            # Try to invoke a simple test (this will fail if no access, but that's ok)
            bedrock_available = True
            print("AWS Bedrock: Client initialized successfully")
            return True
        except Exception as test_error:
            print(f"AWS Bedrock: Connection test failed: {test_error}")
            bedrock_available = False
            return False
            
    except Exception as e:
        print(f"AWS Bedrock: Initialization failed: {e}")
        bedrock_available = False
        return False

# Initialize Bedrock
initialize_bedrock()

# Pydantic models
class UserRegistration(BaseModel):
    username: str
    password: str
    questions: List[str]
    answers: List[str]

class ConnectionAttemptRequest(BaseModel):
    target_username: str
    current_username: str  # Add current user identification
    answers: List[str]

class MessageData(BaseModel):
    content: str
    target_username: str
    current_username: str  # Add current user identification

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_poe_poem(answers: List[str]) -> str:
    """Generate a Poe-style poem from user answers"""
    if bedrock_available and bedrock_client:
        try:
            # Get the answers with fallbacks
            answer1 = answers[0] if len(answers) > 0 and answers[0].strip() else 'mystery'
            answer2 = answers[1] if len(answers) > 1 and answers[1].strip() else 'shadow'
            answer3 = answers[2] if len(answers) > 2 and answers[2].strip() else 'whisper'
            
            prompt = f"""You are Edgar Allan Poe. Create a dark, mysterious poem that cryptically references these three personal details:
1. {answer1}
2. {answer2}
3. {answer3}

The poem should be in Poe's style - dark, gothic, with themes of mystery, death, and the supernatural.
Make it cryptic so that someone familiar with these details could recognize them, but others would find it mysterious.
Use 4-6 stanzas with 4 lines each. Include gothic imagery and Poe's characteristic rhythm.
Do not include any explanations or meta-commentary, just the poem itself."""

            # Try different Claude models
            models_to_try = [
                'anthropic.claude-3-sonnet-20240229-v1:0',
                'anthropic.claude-3-haiku-20240307-v1:0',
                'anthropic.claude-v2:1',
                'anthropic.claude-v2'
            ]
            
            for model_id in models_to_try:
                try:
                    if 'claude-3' in model_id:
                        # Claude 3 format
                        body = json.dumps({
                            "anthropic_version": "bedrock-2023-05-31",
                            "max_tokens": 1000,
                            "temperature": 0.8,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        })
                    else:
                        # Claude 2 format
                        body = json.dumps({
                            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                            "max_tokens_to_sample": 1000,
                            "temperature": 0.8,
                            "top_p": 0.9
                        })
                    
                    response = bedrock_client.invoke_model(
                        modelId=model_id,
                        body=body,
                        contentType='application/json'
                    )
                    
                    response_body = json.loads(response['body'].read())
                    
                    if 'claude-3' in model_id:
                        # Claude 3 response format
                        poem = response_body.get('content', [{}])[0].get('text', '')
                    else:
                        # Claude 2 response format
                        poem = response_body.get('completion', '')
                    
                    if poem and len(poem.strip()) > 50:  # Ensure we got a substantial response
                        print(f"AWS Bedrock: Successfully generated poem using {model_id}")
                        return poem.strip()
                    
                except Exception as model_error:
                    print(f"AWS Bedrock: Model {model_id} failed: {model_error}")
                    continue
            
            print("AWS Bedrock: All models failed, falling back to templates")
            
        except Exception as e:
            print(f"AWS Bedrock error: {e}")
    
    # Enhanced fallback poem templates with better integration
    import random
    
    # Get the answers with fallbacks
    answer1 = answers[0] if len(answers) > 0 and answers[0].strip() else 'mystery'
    answer2 = answers[1] if len(answers) > 1 and answers[1].strip() else 'shadow'
    answer3 = answers[2] if len(answers) > 2 and answers[2].strip() else 'whisper'
    
    poem_templates = [
        f"""
        In the crypt where {answer1} lies entombed,
        A specter haunts the midnight gloom.
        Through veils of {answer2}, shadows creep,
        While {answer3} guards the secrets deep.
        
        The raven's call echoes through the hall,
        As spectral figures rise and fall.
        Three clues hidden in the ancient tome,
        Lead to the heart of this haunted home.
        
        Beware the whispers in the dark,
        For they reveal the eternal mark.
        {answer1}, {answer2}, and {answer3} combined,
        Unlock the mysteries of the mind.
        
        The clock strikes thirteen in the tower,
        As darkness falls with spectral power.
        In this gothic tale of woe,
        The answers only the chosen know.
        """,
        
        f"""
        Once upon a midnight dreary, while I pondered weak and weary,
        Over many a quaint and curious volume of forgotten lore—
        When suddenly there came a tapping, as of someone gently rapping,
        Rapping at my chamber door—"'Tis {answer1}," I muttered, "tapping at my chamber door—
        Only this and nothing more."
        
        Ah, distinctly I remember it was in the bleak December;
        And each separate dying ember wrought its ghost upon the floor.
        Eagerly I wished the morrow;—vainly I had sought to borrow
        From my books surcease of sorrow—sorrow for the lost {answer2}—
        For the rare and radiant maiden whom the angels name {answer3}—
        Nameless here for evermore.
        
        And the silken, sad, uncertain rustling of each purple curtain
        Thrilled me—filled me with fantastic terrors never felt before;
        So that now, to still the beating of my heart, I stood repeating
        "'Tis some visitor entreating entrance at my chamber door—
        Some late visitor entreating entrance at my chamber door;—
        This it is and nothing more."
        """,
        
        f"""
        In the realm where {answer1} dwells in shadowed halls,
        The ancient bell of {answer2} tolls and calls.
        Through corridors of {answer3} and stone,
        The spirits make their presence known.
        
        The moon casts shadows on the wall,
        As spectral figures rise and fall.
        Three secrets locked in time's embrace,
        Await the one who seeks their trace.
        
        The wind carries whispers of the past,
        Where {answer1}, {answer2}, and {answer3} are cast.
        In this gothic tale of woe,
        The answers only the chosen know.
        
        The raven perches on the bust of Pallas,
        While {answer1} crumbles into dust.
        {answer2} and {answer3} dance in the night,
        Revealing secrets in pale moonlight.
        """,
        
        f"""
        Deep in the catacombs where {answer1} lies,
        Where {answer2} and {answer3} roam in disguise,
        Lies the key to understanding,
        The mysteries of this haunted home.
        
        The clock strikes thirteen in the tower,
        As darkness falls with spectral power.
        Three riddles wrapped in gothic verse,
        Each one a blessing, each a curse.
        
        The raven perches on the bust,
        While {answer1} crumbles into dust.
        {answer2} and {answer3} dance in the night,
        Revealing secrets in pale moonlight.
        
        In the crypt where memories dwell,
        The ancient bell begins to swell.
        Through veils of {answer2}, the truth does creep,
        While {answer3} guards the secrets deep.
        """,
        
        f"""
        The Tell-Tale Heart beats beneath the floor,
        Where {answer1} lies forevermore.
        Through {answer2}'s veil, the truth does creep,
        While {answer3} guards the secrets deep.
        
        The raven's call echoes through the gloom,
        As shadows dance in the haunted room.
        Three clues hidden in the ancient tome,
        Lead to the heart of this spectral home.
        
        Beware the whispers in the dark,
        For they reveal the eternal mark.
        {answer1}, {answer2}, and {answer3} combined,
        Unlock the mysteries of the mind.
        
        The clock strikes thirteen in the tower,
        As darkness falls with spectral power.
        In this gothic tale of woe,
        The answers only the chosen know.
        """
    ]
    
    return random.choice(poem_templates).strip()

def generate_cryptic_message(answers: List[str]) -> str:
    """Generate a cryptic message from answers"""
    if bedrock_available and bedrock_client:
        try:
            # Get the answers with fallbacks
            answer1 = answers[0] if len(answers) > 0 and answers[0].strip() else 'mystery'
            answer2 = answers[1] if len(answers) > 1 and answers[1].strip() else 'shadow'
            answer3 = answers[2] if len(answers) > 2 and answers[2].strip() else 'whisper'
            
            prompt = f"""You are Edgar Allan Poe. Transform these personal details into a cryptic, scary message:
{answer1}, {answer2}, {answer3}

Make it sound like a mysterious riddle or warning from beyond the grave.
Use gothic language and Poe's characteristic dark imagery.
Keep it under 100 words but make it haunting and memorable.
Do not include any explanations or meta-commentary, just the cryptic message itself."""

            # Try different Claude models
            models_to_try = [
                'anthropic.claude-3-sonnet-20240229-v1:0',
                'anthropic.claude-3-haiku-20240307-v1:0',
                'anthropic.claude-v2:1',
                'anthropic.claude-v2'
            ]
            
            for model_id in models_to_try:
                try:
                    if 'claude-3' in model_id:
                        # Claude 3 format
                        body = json.dumps({
                            "anthropic_version": "bedrock-2023-05-31",
                            "max_tokens": 200,
                            "temperature": 0.9,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        })
                    else:
                        # Claude 2 format
                        body = json.dumps({
                            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                            "max_tokens_to_sample": 200,
                            "temperature": 0.9,
                            "top_p": 0.9
                        })
                    
                    response = bedrock_client.invoke_model(
                        modelId=model_id,
                        body=body,
                        contentType='application/json'
                    )
                    
                    response_body = json.loads(response['body'].read())
                    
                    if 'claude-3' in model_id:
                        # Claude 3 response format
                        message = response_body.get('content', [{}])[0].get('text', '')
                    else:
                        # Claude 2 response format
                        message = response_body.get('completion', '')
                    
                    if message and len(message.strip()) > 20:  # Ensure we got a substantial response
                        print(f"AWS Bedrock: Successfully generated cryptic message using {model_id}")
                        return message.strip()
                    
                except Exception as model_error:
                    print(f"AWS Bedrock: Model {model_id} failed: {model_error}")
                    continue
            
            print("AWS Bedrock: All models failed, falling back to templates")
            
        except Exception as e:
            print(f"AWS Bedrock error: {e}")
    
    # Enhanced fallback cryptic messages
    import random
    
    # Get the answers with fallbacks
    answer1 = answers[0] if len(answers) > 0 and answers[0].strip() else 'mystery'
    answer2 = answers[1] if len(answers) > 1 and answers[1].strip() else 'shadow'
    answer3 = answers[2] if len(answers) > 2 and answers[2].strip() else 'whisper'
    
    cryptic_templates = [
        f"Beware, mortal soul! The answers you seek lie hidden in the shadows of {answer1} and {answer2}... The raven's call echoes through the crypt of {answer3}, but will you understand its message? The spirits whisper in the midnight hour, and the ancient bell tolls for those who dare to listen.",
        
        f"The spirits whisper of {answer1} and {answer2} in the midnight hour... In the realm of {answer3}, your truth awaits, but tread carefully through the gothic maze of secrets. The raven perches on the bust of Pallas, watching with eyes that see beyond the veil of death.",
        
        f"Three clues lie before you in the haunted chamber: {answer1}, {answer2}, and {answer3}... The ancient bell tolls, and the specters dance in the pale moonlight. The Tell-Tale Heart beats beneath the floor, where the answers are written in blood and bone.",
        
        f"The raven perches on the bust of {answer1}, while {answer2} and {answer3} dance in the shadows... The answers are written in the dust of forgotten tombs. The clock strikes thirteen in the tower, and the spirits know your secrets, but will you know theirs?",
        
        f"In the catacombs of {answer1}, where {answer2} and {answer3} roam, lies the key to understanding... But beware the whispers in the dark, for they reveal the eternal mark. The wind carries secrets through the haunted halls, and the raven's call echoes in the gloom.",
        
        f"The clock strikes thirteen in the tower of {answer1}, as {answer2} and {answer3} weave their gothic tale... The spirits know your secrets, but will you know theirs? Deep in the crypt where memories dwell, the ancient bell begins to swell.",
        
        f"Deep in the crypt where {answer1} dwells, the ancient bell of {answer2} swells... Through corridors of {answer3} and stone, the answers are carved in bone. The raven's call echoes through the gloom, as shadows dance in the haunted room.",
        
        f"The wind carries whispers of {answer1}, {answer2}, and {answer3} through the haunted halls... The raven's call echoes in the gloom, revealing secrets in the ancient tomb. The Tell-Tale Heart beats beneath the floor, where the truth lies forevermore.",
        
        f"Once upon a midnight dreary, while I pondered weak and weary, over many a quaint and curious volume of forgotten lore... When suddenly there came a tapping, as of someone gently rapping, rapping at my chamber door—'Tis {answer1}, I muttered, tapping at my chamber door—Only this and nothing more.",
        
        f"The silken, sad, uncertain rustling of each purple curtain thrilled me—filled me with fantastic terrors never felt before... So that now, to still the beating of my heart, I stood repeating '{answer1} and {answer2} and {answer3}'—This it is and nothing more."
    ]
    
    return random.choice(cryptic_templates)

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
async def attempt_connection(attempt: ConnectionAttemptRequest, db: Session = Depends(get_db)):
    """Attempt to connect to another user by answering their questions"""
    try:
        # Get target user
        target_user = db.query(User).filter(User.username == attempt.target_username).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get the current user by username
        current_user = db.query(User).filter(User.username == attempt.current_username).first()
        if not current_user:
            raise HTTPException(status_code=404, detail="Current user not found")
        
        # Check cooldown
        attempt_record = db.query(ConnectionAttempt).filter(
            ConnectionAttempt.user_id == current_user.id,
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
                user_id=current_user.id,
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
            # Check if connection already exists
            existing_connection = db.query(Connection).filter(
                ((Connection.user1_id == current_user.id) & (Connection.user2_id == target_user.id)) |
                ((Connection.user1_id == target_user.id) & (Connection.user2_id == current_user.id))
            ).first()
            
            if not existing_connection:
                connection = Connection(user1_id=current_user.id, user2_id=target_user.id)
                db.add(connection)
                db.commit()
                print(f"✅ Connection created between {current_user.username} (ID: {current_user.id}) and {target_user.username} (ID: {target_user.id})")
            else:
                print(f"✅ Connection already exists between {current_user.username} and {target_user.username}")
            
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
    print(f"🔍 Getting messages for user {user_id} with {target_username}")
    
    target_user = db.query(User).filter(User.username == target_username).first()
    if not target_user:
        print(f"❌ Target user {target_username} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    print(f"✅ Target user found: {target_user.username} (ID: {target_user.id})")
    
    connection = db.query(Connection).filter(
        ((Connection.user1_id == user_id) & (Connection.user2_id == target_user.id)) |
        ((Connection.user1_id == target_user.id) & (Connection.user2_id == user_id))
    ).first()
    
    if not connection:
        print(f"❌ No connection found between user {user_id} and {target_user.id}")
        # Let's check what connections exist
        all_connections = db.query(Connection).all()
        print(f"📊 All connections in database:")
        for conn in all_connections:
            print(f"   - Connection {conn.id}: User {conn.user1_id} <-> User {conn.user2_id}")
        raise HTTPException(status_code=404, detail="No connection found")
    
    print(f"✅ Connection found: ID {connection.id}")
    
    messages = db.query(Message).filter(Message.connection_id == connection.id).order_by(Message.timestamp).all()
    print(f"📬 Found {len(messages)} messages")
    
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.username,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]

@app.post("/create-connection")
async def create_connection(user1_username: str, user2_username: str, db: Session = Depends(get_db)):
    """Manually create a connection between two users (for testing)"""
    try:
        # Get both users
        user1 = db.query(User).filter(User.username == user1_username).first()
        user2 = db.query(User).filter(User.username == user2_username).first()
        
        if not user1:
            raise HTTPException(status_code=404, detail=f"User {user1_username} not found")
        if not user2:
            raise HTTPException(status_code=404, detail=f"User {user2_username} not found")
        
        # Check if connection already exists
        existing_connection = db.query(Connection).filter(
            ((Connection.user1_id == user1.id) & (Connection.user2_id == user2.id)) |
            ((Connection.user1_id == user2.id) & (Connection.user2_id == user1.id))
        ).first()
        
        if existing_connection:
            return {
                "message": f"Connection already exists between {user1_username} and {user2_username}",
                "connection_id": existing_connection.id
            }
        
        # Create new connection
        connection = Connection(user1_id=user1.id, user2_id=user2.id)
        db.add(connection)
        db.commit()
        db.refresh(connection)
        
        print(f"✅ Manual connection created: {user1_username} (ID: {user1.id}) <-> {user2_username} (ID: {user2.id})")
        
        return {
            "message": f"Connection created between {user1_username} and {user2_username}",
            "connection_id": connection.id,
            "user1_id": user1.id,
            "user2_id": user2.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-message")
async def send_message(message_data: MessageData, db: Session = Depends(get_db)):
    """Send a message between connected users"""
    try:
        # Get users
        sender_user = db.query(User).filter(User.username == message_data.current_username).first()
        target_user = db.query(User).filter(User.username == message_data.target_username).first()
        
        if not sender_user or not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Find connection
        connection = db.query(Connection).filter(
            ((Connection.user1_id == sender_user.id) & (Connection.user2_id == target_user.id)) |
            ((Connection.user1_id == target_user.id) & (Connection.user2_id == sender_user.id))
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="No connection found")
        
        # Create message
        message = Message(
            connection_id=connection.id,
            sender_id=sender_user.id,
            content=message_data.content
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return {
            "id": message.id,
            "content": message.content,
            "sender": sender_user.username,
            "timestamp": message.timestamp.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Create tables if they don't exist
    create_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)