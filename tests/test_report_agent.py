#!/usr/bin/env python3
"""
Test Report Agent - Create sample data and test report generation.

This script creates sample learning data for testing the Report Agent
and demonstrates various report generation capabilities.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database.database import SessionLocal, initialize_database
from database.models import (
    User, QuizSession, Question, UserResponse,
    ProgressSnapshot, QuizAttemptHistory, TopicMastery, LearningSession
)
from agents.report.agent import ReportAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_sample_user(db, session_id: str = "test_user_report_123"):
    """Create a sample user for testing."""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        user = User(session_id=session_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Created user: {user.id}")
    else:
        logger.info(f"Using existing user: {user.id}")
        # Clean up old test data for this user
        cleanup_user_data(db, user.id)
    return user


def cleanup_user_data(db, user_id: int):
    """Clean up existing test data for a user."""
    logger.info(f"Cleaning up old test data for user {user_id}...")
    
    # Get all quiz sessions for this user
    quiz_sessions = db.query(QuizSession).filter(QuizSession.user_id == user_id).all()
    quiz_session_ids = [qs.id for qs in quiz_sessions]
    
    # Delete user responses (need to import here to avoid circular reference)
    from database.models import UserResponse as UR
    if quiz_session_ids:
        db.query(UR).filter(UR.quiz_session_id.in_(quiz_session_ids)).delete(synchronize_session=False)
    
    # Delete quiz attempt history
    db.query(QuizAttemptHistory).filter(QuizAttemptHistory.user_id == user_id).delete(synchronize_session=False)
    
    # Delete quiz sessions
    db.query(QuizSession).filter(QuizSession.user_id == user_id).delete(synchronize_session=False)
    
    # Delete progress snapshots
    db.query(ProgressSnapshot).filter(ProgressSnapshot.user_id == user_id).delete(synchronize_session=False)
    
    # Delete topic mastery
    db.query(TopicMastery).filter(TopicMastery.user_id == user_id).delete(synchronize_session=False)
    
    # Delete learning sessions
    db.query(LearningSession).filter(LearningSession.user_id == user_id).delete(synchronize_session=False)
    
    db.commit()
    logger.info(f"✓ Cleaned up old data for user {user_id}")


def create_sample_progress_data(db, user_id: int, days: int = 14):
    """Create sample progress snapshots over time."""
    logger.info(f"Creating {days} days of progress snapshots...")
    
    topics = ["probability", "statistics", "combinatorics", "distributions"]
    
    for day in range(days, 0, -1):
        snapshot_date = datetime.utcnow() - timedelta(days=day)
        
        # Simulate improving performance over time
        base_accuracy = 50 + (days - day) * 2  # Gradual improvement
        noise = random.uniform(-5, 5)  # Add some variance
        overall_accuracy = min(95, max(40, base_accuracy + noise))
        
        # Calculate ability score from accuracy
        ability_score = overall_accuracy / 100
        
        # Difficulty breakdown
        easy_accuracy = min(100, overall_accuracy + 10)
        medium_accuracy = overall_accuracy
        difficult_accuracy = max(30, overall_accuracy - 15)
        
        # Topic scores
        topic_scores = {
            topic: min(100, max(30, overall_accuracy + random.uniform(-10, 10)))
            for topic in topics
        }
        
        snapshot = ProgressSnapshot(
            user_id=user_id,
            snapshot_date=snapshot_date,
            overall_accuracy=overall_accuracy,
            ability_score=ability_score,
            competence_level="medium" if 60 <= overall_accuracy < 80 else "easy" if overall_accuracy < 60 else "difficult",
            easy_accuracy=easy_accuracy,
            medium_accuracy=medium_accuracy,
            difficult_accuracy=difficult_accuracy,
            total_questions_attempted=(days - day + 1) * 25,
            total_questions_correct=int(((days - day + 1) * 25) * (overall_accuracy / 100)),
            topic_scores=topic_scores,
            total_learning_time_minutes=(days - day + 1) * 45,
            quiz_attempts_count=days - day + 1,
            snapshot_type="daily"
        )
        
        db.add(snapshot)
    
    db.commit()
    logger.info(f"✓ Created {days} progress snapshots")


def create_sample_quiz_history(db, user_id: int, quiz_count: int = 10):
    """Create sample quiz attempt history."""
    logger.info(f"Creating {quiz_count} quiz attempts...")
    
    topics = ["probability", "statistics", "combinatorics", "distributions"]
    
    # Create a quiz session first
    for i in range(quiz_count):
        attempt_date = datetime.utcnow() - timedelta(days=quiz_count - i)
        
        # Improving scores over time
        base_score = 50 + i * 4
        score = min(95, max(40, base_score + random.uniform(-5, 5)))
        
        total_questions = 25
        correct_answers = int(total_questions * (score / 100))
        
        # Create quiz session
        quiz_session = QuizSession(
            user_id=user_id,
            session_id=f"quiz_session_{user_id}_{i}",
            current_question_number=total_questions,
            total_questions=total_questions,
            is_completed=True,
            started_at=attempt_date,
            completed_at=attempt_date + timedelta(minutes=random.randint(15, 30)),
            easy_correct=int(correct_answers * 0.4),
            easy_total=int(total_questions * 0.4),
            medium_correct=int(correct_answers * 0.4),
            medium_total=int(total_questions * 0.4),
            difficult_correct=int(correct_answers * 0.2),
            difficult_total=int(total_questions * 0.2),
        )
        db.add(quiz_session)
        db.commit()
        db.refresh(quiz_session)
        
        # Create quiz attempt history
        quiz_attempt = QuizAttemptHistory(
            user_id=user_id,
            quiz_session_id=quiz_session.id,
            attempted_at=attempt_date,
            duration_minutes=random.uniform(15, 30),
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            easy_correct=quiz_session.easy_correct,
            easy_total=quiz_session.easy_total,
            medium_correct=quiz_session.medium_correct,
            medium_total=quiz_session.medium_total,
            difficult_correct=quiz_session.difficult_correct,
            difficult_total=quiz_session.difficult_total,
            topics=random.sample(topics, k=random.randint(2, 4)),
            topic_scores={
                topic: min(100, max(30, score + random.uniform(-10, 10)))
                for topic in topics
            },
            quiz_type="practice" if i < quiz_count - 1 else "assessment"
        )
        
        db.add(quiz_attempt)
    
    db.commit()
    logger.info(f"✓ Created {quiz_count} quiz attempts")


def create_sample_topic_mastery(db, user_id: int):
    """Create sample topic mastery records."""
    logger.info("Creating topic mastery records...")
    
    topics_data = [
        ("probability", 0.85, "mastered", 30, 25),
        ("statistics", 0.72, "learning", 25, 18),
        ("combinatorics", 0.65, "learning", 20, 13),
        ("distributions", 0.55, "learning", 15, 8),
        ("conditional_probability", 0.45, "learning", 10, 4),
    ]
    
    for topic, mastery_level, status, total, correct in topics_data:
        mastery = TopicMastery(
            user_id=user_id,
            topic=topic,
            mastery_level=mastery_level,
            confidence_score=mastery_level * 0.9,  # Slightly lower than mastery
            attempts=total,
            correct_count=correct,
            total_count=total,
            first_attempted=datetime.utcnow() - timedelta(days=14),
            last_attempted=datetime.utcnow() - timedelta(days=1),
            mastery_history=[
                {"date": (datetime.utcnow() - timedelta(days=14-i)).isoformat(), "level": min(1.0, mastery_level - 0.3 + (i * 0.03))}
                for i in range(10)
            ],
            status=status
        )
        db.add(mastery)
    
    db.commit()
    logger.info(f"✓ Created {len(topics_data)} topic mastery records")


def create_sample_learning_sessions(db, user_id: int, session_count: int = 15):
    """Create sample learning sessions."""
    logger.info(f"Creating {session_count} learning sessions...")
    
    for i in range(session_count):
        session_date = datetime.utcnow() - timedelta(days=session_count - i)
        duration = random.uniform(20, 60)
        
        session = LearningSession(
            user_id=user_id,
            started_at=session_date,
            ended_at=session_date + timedelta(minutes=duration),
            duration_minutes=duration,
            activities=[
                {"type": "quiz", "topic": "probability", "duration": 15},
                {"type": "study", "topic": "statistics", "duration": duration - 15}
            ],
            topics_covered=["probability", "statistics"],
            questions_attempted=random.randint(10, 25),
            questions_correct=random.randint(5, 20),
            content_pages_viewed=random.randint(3, 10),
            session_type="study" if i % 3 == 0 else "practice"
        )
        db.add(session)
    
    db.commit()
    logger.info(f"✓ Created {session_count} learning sessions")


def test_report_generation(user_session_id: str):
    """Test various report generation functions."""
    print("\n" + "=" * 80)
    print("TESTING REPORT AGENT")
    print("=" * 80)
    
    # Create Report Agent
    print("\nCreating Report Agent...")
    agent = ReportAgent()
    print("✓ Report Agent created")
    
    # # Test 1: Comprehensive Report
    # print("\n" + "=" * 80)
    # print("TEST 1: COMPREHENSIVE REPORT (7 days)")
    # print("=" * 80)
    # report = agent.generate_report(user_session_id, days=7, report_type="comprehensive")
    # print(report)
    
    # # Test 2: Quick Summary
    # print("\n" + "=" * 80)
    # print("TEST 2: QUICK SUMMARY (7 days)")
    # print("=" * 80)
    # report = agent.generate_report(user_session_id, days=7, report_type="quick")
    # print(report)
    
    # # Test 3: Progress Analysis
    # print("\n" + "=" * 80)
    # print("TEST 3: PROGRESS ANALYSIS (14 days)")
    # print("=" * 80)
    # analysis = agent.analyze_progress(user_session_id, days=14)
    # print(analysis)
    
    # # Test 4: Recommendations
    # print("\n" + "=" * 80)
    # print("TEST 4: PERSONALIZED RECOMMENDATIONS")
    # print("=" * 80)
    # recommendations = agent.get_recommendations(user_session_id)
    # print(recommendations)
    
    # # Test 5: Period Comparison
    # print("\n" + "=" * 80)
    # print("TEST 5: TIME PERIOD COMPARISON")
    # print("=" * 80)
    # comparison = agent.compare_periods(user_session_id, recent_days=7, previous_days=14)
    # print(comparison)
    
    # Test 6: Visualizations (Text Format)
    print("\n" + "=" * 80)
    print("TEST 6: PROGRESS VISUALIZATIONS (Text Format)")
    print("=" * 80)
    visualizations = agent.get_visualizations(user_session_id, days=14, format="markdown")
    print(visualizations)
    
    # Test 7: Visualizations (JSON Format)
    print("\n" + "=" * 80)
    print("TEST 7: VISUALIZATION DATA (JSON Format)")
    print("=" * 80)
    viz_json = agent.get_visualizations(user_session_id, days=14, format="json")
    print(viz_json[:1000] + "..." if len(viz_json) > 1000 else viz_json)  # Truncate for readability


def main():
    """Main test function."""
    print("=" * 80)
    print("REPORT AGENT - TEST WITH SAMPLE DATA")
    print("=" * 80)
    
    # Initialize database
    print("\nInitializing database...")
    initialize_database()
    print("✓ Database initialized")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create sample user
        print("\nCreating sample user...")
        user_session_id = "test_user_report_123"
        user = create_sample_user(db, user_session_id)
        print(f"✓ User created with ID: {user.id}")
        
        # Create sample data
        print("\n" + "=" * 80)
        print("CREATING SAMPLE LEARNING DATA")
        print("=" * 80)
        
        create_sample_progress_data(db, user.id, days=14)
        create_sample_quiz_history(db, user.id, quiz_count=10)
        create_sample_topic_mastery(db, user.id)
        create_sample_learning_sessions(db, user.id, session_count=15)
        
        print("\n✓ All sample data created successfully!")
        
        # Test report generation
        test_report_generation(user_session_id)
        
    except Exception as e:
        logger.error(f"Error in test: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
    finally:
        db.close()
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
