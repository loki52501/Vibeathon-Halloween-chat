from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Halloween Poe Chat API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def init_db():
    conn = sqlite3.connect('poe_chat.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            questions TEXT NOT NULL,
            answers TEXT NOT NULL,
            poem TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connection_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            target_user_id INTEGER,
            attempts INTEGER DEFAULT 0,
            last_attempt TIMESTAMP,
            cooldown_until TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (target_user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER,
            user2_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user1_id) REFERENCES users (id),
            FOREIGN KEY (user2_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Pydantic models
class UserRegistration(BaseModel):
    username: str
    password: str
    questions: List[str]
    answers: List[str]

class ConnectionAttempt(BaseModel):
    target_username: str
    answers: List[str]

# Initialize database
init_db()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_poe_poem(answers: List[str]) -> str:
    """Generate a Poe-style poem from user answers (fallback version)"""
    poem_templates = [
        f"""
        In shadows deep where memories dwell,
        Three secrets hidden, none can tell.
        {answers[0] if len(answers) > 0 else 'Whispers'} echo through the night,
        {answers[1] if len(answers) > 1 else 'Dreams'} fade into pale moonlight.
        
        {answers[2] if len(answers) > 2 else 'Silence'} speaks in hollow tones,
        Through haunted halls and ancient stones.
        The raven's call, the midnight chime,
        These secrets lost in endless time.
        """,
        f"""
        Once upon a midnight dreary, while I pondered weak and weary,
        Over many a quaint and curious volume of forgotten lore—
        When suddenly there came a tapping, as of someone gently rapping,
        Rapping at my chamber door—"'Tis {answers[0] if len(answers) > 0 else 'some visitor'}," I muttered, "tapping at my chamber door—
        Only this and nothing more."
        
        Ah, distinctly I remember it was in the bleak December;
        And each separate dying ember wrought its ghost upon the floor.
        Eagerly I wished the morrow;—vainly I had sought to borrow
        From my books surcease of sorrow—sorrow for the lost {answers[1] if len(answers) > 1 else 'Lenore'}—
        For the rare and radiant maiden whom the angels name {answers[2] if len(answers) > 2 else 'Lenore'}—
        Nameless here for evermore.
        """,
        f"""
        In the kingdom by the sea,
        Where the maiden lived with me,
        {answers[0] if len(answers) > 0 else 'Love'} was all we knew,
        {answers[1] if len(answers) > 1 else 'Dreams'} so pure and true.
        
        But the angels, not half so happy in heaven,
        Went envying her and me—
        Yes!—that was the reason (as all men know,
        In this kingdom by the sea)
        That the wind came out of the cloud by night,
        Chilling and killing my {answers[2] if len(answers) > 2 else 'Annabel Lee'}.
        """
    ]
    
    import random
    return random.choice(poem_templates).strip()

def generate_cryptic_message(answers: List[str]) -> str:
    """Generate a cryptic message from answers (fallback version)"""
    cryptic_templates = [
        f"Beware, mortal! The answers you seek lie hidden in the shadows of {', '.join(answers[:2])}...",
        f"The spirits whisper of {answers[0] if len(answers) > 0 else 'secrets'} and {answers[1] if len(answers) > 1 else 'mysteries'}...",
        f"In the realm of {answers[2] if len(answers) > 2 else 'darkness'}, your truth awaits...",
        f"The raven knows of {', '.join(answers)}... but will you understand its message?",
        f"Three clues lie before you: {answers[0] if len(answers) > 0 else 'shadow'}, {answers[1] if len(answers) > 1 else 'mystery'}, and {answers[2] if len(answers) > 2 else 'truth'}..."
    ]
    
    import random
    return random.choice(cryptic_templates)

@app.post("/register")
async def register_user(user_data: UserRegistration):
    """Register a new user with their questions and answers"""
    conn = sqlite3.connect('poe_chat.db')
    cursor = conn.cursor()
    
    try:
        # Check if username exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (user_data.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Generate poem from answers
        poem = generate_poe_poem(user_data.answers)
        
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Insert user
        cursor.execute("""
            INSERT INTO users (username, password_hash, questions, answers, poem)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_data.username,
            password_hash,
            json.dumps(user_data.questions),
            json.dumps(user_data.answers),
            poem
        ))
        
        conn.commit()
        user_id = cursor.lastrowid
        
        return {
            "message": "User registered successfully",
            "user_id": user_id,
            "poem": poem
        }
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/users")
async def get_users():
    """Get list of all users (for connection attempts)"""
    conn = sqlite3.connect('poe_chat.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, poem FROM users")
    users = cursor.fetchall()
    
    conn.close()
    
    return [{"id": user[0], "username": user[1], "poem": user[2]} for user in users]

@app.post("/attempt-connection")
async def attempt_connection(attempt: ConnectionAttempt):
    """Attempt to connect to another user by answering their questions"""
    conn = sqlite3.connect('poe_chat.db')
    cursor = conn.cursor()
    
    try:
        # Get target user
        cursor.execute("SELECT id, answers FROM users WHERE username = ?", (attempt.target_username,))
        target_user = cursor.fetchone()
        
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        target_user_id, target_answers_json = target_user
        target_answers = json.loads(target_answers_json)
        
        # Check cooldown
        cursor.execute("""
            SELECT attempts, cooldown_until FROM connection_attempts 
            WHERE user_id = ? AND target_user_id = ?
        """, (1, target_user_id))  # Assuming user_id = 1 for now
        
        attempt_record = cursor.fetchone()
        
        if attempt_record:
            attempts, cooldown_until = attempt_record
            if cooldown_until and datetime.fromisoformat(cooldown_until) > datetime.now():
                remaining_time = datetime.fromisoformat(cooldown_until) - datetime.now()
                raise HTTPException(
                    status_code=429, 
                    detail=f"Cooldown active. Try again in {remaining_time.seconds} seconds"
                )
            
            if attempts >= 5:
                # Set 2-minute cooldown
                cooldown_until = datetime.now() + timedelta(minutes=2)
                cursor.execute("""
                    UPDATE connection_attempts 
                    SET attempts = 0, cooldown_until = ?
                    WHERE user_id = ? AND target_user_id = ?
                """, (cooldown_until.isoformat(), 1, target_user_id))
                conn.commit()
                raise HTTPException(status_code=429, detail="Too many attempts. 2-minute cooldown activated.")
        
        # Check answers
        correct_answers = 0
        for i, answer in enumerate(attempt.answers):
            if i < len(target_answers) and answer.lower().strip() == target_answers[i].lower().strip():
                correct_answers += 1
        
        # Update attempt record
        if attempt_record:
            cursor.execute("""
                UPDATE connection_attempts 
                SET attempts = attempts + 1, last_attempt = ?
                WHERE user_id = ? AND target_user_id = ?
            """, (datetime.now().isoformat(), 1, target_user_id))
        else:
            cursor.execute("""
                INSERT INTO connection_attempts (user_id, target_user_id, attempts, last_attempt)
                VALUES (?, ?, 1, ?)
            """, (1, target_user_id, datetime.now().isoformat()))
        
        conn.commit()
        
        # Generate cryptic message
        cryptic_message = generate_cryptic_message(attempt.answers)
        
        if correct_answers == 3:
            # All answers correct - create connection
            cursor.execute("""
                INSERT INTO connections (user1_id, user2_id)
                VALUES (?, ?)
            """, (1, target_user_id))
            conn.commit()
            
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
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/connections/{user_id}")
async def get_connections(user_id: int):
    """Get user's connections"""
    conn = sqlite3.connect('poe_chat.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.username FROM connections c
        JOIN users u ON (c.user1_id = u.id OR c.user2_id = u.id)
        WHERE (c.user1_id = ? OR c.user2_id = ?) AND u.id != ?
    """, (user_id, user_id, user_id))
    
    connections = cursor.fetchall()
    conn.close()
    
    return [{"username": conn[0]} for conn in connections]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
