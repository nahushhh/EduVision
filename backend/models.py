from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    session_type = Column(String) # "discovery", "quiz"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ImageRecognitionLog(Base):
    __tablename__ = "image_recognition_log"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, index=True)
    image_path = Column(String)
    parent_category = Column(String)
    child_category = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EngagementLog(Base):
    __tablename__ = "engagement_log"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, index=True)
    state = Column(String) # "Engaged", "Confused", "Bored"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
