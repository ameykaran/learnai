from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from agents.onboarding.backend.models import Base, Question
from agents.onboarding.backend.questions_data import questions_data

import logging
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./quiz.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database():
    """Initialize database and populate questions if needed"""
    create_tables()

    # Check if questions are already populated
    db = next(get_db())
    existing_questions = db.query(Question).count()

    if existing_questions == 0:
        # Populate questions from questions_data
        for q_data in questions_data:
            question = Question(**q_data)
            db.add(question)
        db.commit()
        logging.info(
            f"Populated database with {len(questions_data)} questions")
    else:
        logging.info(
            f"Database already contains {existing_questions} questions")

    db.close()
