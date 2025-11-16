from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    created_at = Column(DateTime, default=datetime.now)

    quiz_sessions = relationship("QuizSession", back_populates="user")

class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), unique=True, nullable=False)
    current_question_number = Column(Integer, default=1)
    total_questions = Column(Integer, default=int(os.getenv('ONBOARDING_TOTAL_QUESTIONS', '25')))

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
    started_at = Column(DateTime, default=datetime.now)
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
    answered_at = Column(DateTime, default=datetime.now)
    time_taken_seconds = Column(Integer, nullable=True)

    quiz_session = relationship("QuizSession", back_populates="user_responses")
    question = relationship("Question", back_populates="user_responses")


# ============================================================================
# TIME-SERIES TRACKING MODELS FOR PROGRESS REPORTING
# ============================================================================

class ProgressSnapshot(Base):
    """
    Stores periodic snapshots of student progress for time-series analysis.
    Captures overall performance metrics at specific points in time.
    """
    __tablename__ = "progress_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    snapshot_date = Column(DateTime, default=datetime.now, index=True)
    
    # Performance metrics
    overall_accuracy = Column(Float, default=0.0)  # 0-100
    ability_score = Column(Float, default=0.0)  # 0-1 (IRT-based)
    competence_level = Column(String(20), nullable=True)  # easy/medium/difficult
    
    # Difficulty breakdown
    easy_accuracy = Column(Float, default=0.0)
    medium_accuracy = Column(Float, default=0.0)
    difficult_accuracy = Column(Float, default=0.0)
    
    # Question counts
    total_questions_attempted = Column(Integer, default=0)
    total_questions_correct = Column(Integer, default=0)
    
    # Topic-specific data (JSON)
    topic_scores = Column(JSON, nullable=True)  # {"probability": 0.85, "statistics": 0.72, ...}
    
    # Learning activity
    total_learning_time_minutes = Column(Float, default=0.0)
    quiz_attempts_count = Column(Integer, default=0)
    
    # Metadata
    snapshot_type = Column(String(20), default="daily")  # daily, weekly, monthly
    notes = Column(Text, nullable=True)

    user = relationship("User", backref="progress_snapshots")


class QuizAttemptHistory(Base):
    """
    Historical record of all quiz attempts with detailed performance data.
    Links to QuizSession but stores summary data for fast querying.
    """
    __tablename__ = "quiz_attempt_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    
    # Timing
    attempted_at = Column(DateTime, default=datetime.now, index=True)
    duration_minutes = Column(Float, default=0.0)
    
    # Performance
    score = Column(Float, default=0.0)  # 0-100
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    
    # Difficulty distribution
    easy_correct = Column(Integer, default=0)
    easy_total = Column(Integer, default=0)
    medium_correct = Column(Integer, default=0)
    medium_total = Column(Integer, default=0)
    difficult_correct = Column(Integer, default=0)
    difficult_total = Column(Integer, default=0)
    
    # Topics covered
    topics = Column(JSON, nullable=True)  # ["probability", "statistics", ...]
    topic_scores = Column(JSON, nullable=True)  # {"probability": 0.8, ...}
    
    # Quiz type
    quiz_type = Column(String(50), default="practice")  # onboarding, practice, assessment
    
    user = relationship("User", backref="quiz_history")
    quiz_session = relationship("QuizSession", backref="attempt_history")


class TopicMastery(Base):
    """
    Tracks student mastery level for each topic over time.
    Updated after each quiz or learning session.
    """
    __tablename__ = "topic_mastery"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(100), nullable=False, index=True)
    
    # Current mastery level
    mastery_level = Column(Float, default=0.0)  # 0-1 scale
    confidence_score = Column(Float, default=0.0)  # 0-1 scale
    
    # Performance history
    attempts = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    
    # Timing
    first_attempted = Column(DateTime, default=datetime.now)
    last_attempted = Column(DateTime, default=datetime.now, index=True)
    
    # Progress tracking
    mastery_history = Column(JSON, nullable=True)  # [{"date": "...", "level": 0.5}, ...]
    
    # Status
    status = Column(String(20), default="learning")  # learning, mastered, needs_review
    
    user = relationship("User", backref="topic_mastery")


class LearningSession(Base):
    """
    Tracks individual learning sessions (study time, activities, engagement).
    """
    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Session timing
    started_at = Column(DateTime, default=datetime.now, index=True)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Float, default=0.0)
    
    # Activities
    activities = Column(JSON, nullable=True)  # [{"type": "quiz", "topic": "...", ...}, ...]
    
    # Topics covered
    topics_covered = Column(JSON, nullable=True)  # ["probability", "statistics"]
    
    # Engagement metrics
    questions_attempted = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)
    content_pages_viewed = Column(Integer, default=0)
    
    # Session type
    session_type = Column(String(50), default="general")  # quiz, study, practice, review
    
    user = relationship("User", backref="learning_sessions")