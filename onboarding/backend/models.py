from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False)
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)
    correct_answer = Column(String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    difficulty = Column(String(10), nullable=False)  # 'easy', 'medium', 'difficult'
    grade_level = Column(String(10), nullable=False)  # '7-8', '9-10', '11-12'
    topic = Column(String(100), nullable=False)

    user_responses = relationship("UserResponse", back_populates="question")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    quiz_sessions = relationship("QuizSession", back_populates="user")

class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), unique=True, nullable=False)
    current_question_number = Column(Integer, default=1)
    total_questions = Column(Integer, default=25)

    # New adaptive algorithm fields
    ability = Column(Float, default=0.25)  # Current ability estimate [0,1]
    asked_ids = Column(JSON, default=list)  # List of question IDs already asked
    medium_seen = Column(Integer, default=0)  # Count of medium questions asked
    difficult_seen = Column(Integer, default=0)  # Count of difficult questions asked
    history = Column(JSON, default=list)  # List of question history with details
    final_ability = Column(Float, nullable=True)  # Final ability score for debugging

    # Keep legacy fields for backwards compatibility and stats
    current_difficulty = Column(String(10), default="easy")
    easy_correct = Column(Integer, default=0)
    medium_correct = Column(Integer, default=0)
    difficult_correct = Column(Integer, default=0)
    easy_total = Column(Integer, default=0)
    medium_total = Column(Integer, default=0)
    difficult_total = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    final_competence_level = Column(String(10), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="quiz_sessions")
    user_responses = relationship("UserResponse", back_populates="quiz_session")

class UserResponse(Base):
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True, index=True)
    quiz_session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    is_correct = Column(Boolean, nullable=False)
    question_number = Column(Integer, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)
    time_taken_seconds = Column(Integer, nullable=True)

    quiz_session = relationship("QuizSession", back_populates="user_responses")
    question = relationship("Question", back_populates="user_responses")