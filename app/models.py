from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    username = Column(String(100))
    avatar = Column(String(255))
    last_seen = Column(DateTime, default=datetime.utcnow)
    online = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    type = Column(String(20), default='private')
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatParticipant(Base):
    __tablename__ = 'chat_participants'
    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String(20), default='text')
    content = Column(Text)
    file_hash = Column(String(64))
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='sent')