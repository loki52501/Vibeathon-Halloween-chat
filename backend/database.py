"""
Database configuration and models for Halloween Poe Chat
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'poe_chat')}"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    questions = Column(Text, nullable=False)  # JSON string
    answers = Column(Text, nullable=False)    # JSON string
    poem = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships - specify foreign_keys to avoid ambiguity
    connection_attempts = relationship("ConnectionAttempt", foreign_keys="ConnectionAttempt.user_id", back_populates="user")
    target_attempts = relationship("ConnectionAttempt", foreign_keys="ConnectionAttempt.target_user_id", back_populates="target_user")
    connections1 = relationship("Connection", foreign_keys="Connection.user1_id", back_populates="user1")
    connections2 = relationship("Connection", foreign_keys="Connection.user2_id", back_populates="user2")
    messages = relationship("Message", back_populates="sender")

class ConnectionAttempt(Base):
    __tablename__ = "connection_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    attempts = Column(Integer, default=0)
    last_attempt = Column(DateTime)
    cooldown_until = Column(DateTime)
    
    # Relationships - specify foreign_keys explicitly
    user = relationship("User", foreign_keys=[user_id], back_populates="connection_attempts")
    target_user = relationship("User", foreign_keys=[target_user_id], back_populates="target_attempts")

class Connection(Base):
    __tablename__ = "connections"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships - specify foreign_keys explicitly
    user1 = relationship("User", foreign_keys=[user1_id], back_populates="connections1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="connections2")
    messages = relationship("Message", back_populates="connection")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    
    # Relationships - specify foreign_keys explicitly
    connection = relationship("Connection", foreign_keys=[connection_id], back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages")

class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String(100), unique=True, index=True, nullable=False)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships - specify foreign_keys explicitly
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Drop all tables (for testing)
def drop_tables():
    Base.metadata.drop_all(bind=engine)
