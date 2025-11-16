#!/usr/bin/env python3
"""
Populate Learning History - Auto-generate sample learning data for any user.

This script creates realistic learning history data for testing the Report Agent.
Use this to populate data for a new user profile created in the frontend.

Usage:
    python3 populate_learning_history.py <session_id> [days]
    
Examples:
    python3 populate_learning_history.py user_abc123
    python3 populate_learning_history.py user_abc123 30
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


def find_or_create_user(db, session_id: str):
    """Find existing user or create new one."""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        logger.error(f"❌ User not found with session_id: {session_id}")
        logger.info(f"💡 This user hasn't completed onboarding yet.")
        logger.info(f"   1. Go to http://localhost:3000")
        logger.info(f"   2. Complete the assessment")
        logger.info(f"   3. Then run this script again with the session_id from the URL")
        return None
    
    logger.info(f"✓ Found user: {user.id} (session: {session_id})")
    return user


def cleanup_existing_data(db, user_id: int, session_id: str):
    """Clean up existing learning history data."""
    response = input(f"\n⚠️  User {session_id} may have existing data. Clean it up? (y/N): ")
    
    if response.lower() != 'y':
        logger.info("Keeping existing data. Will add to it.")
        return False
    
    logger.info(f"Cleaning up existing data for user {user_id}...")
    
    # Get all quiz sessions
    quiz_sessions = db.query(QuizSession).filter(QuizSession.user_id == user_id).all()
    quiz_session_ids = [qs.id for qs in quiz_sessions]
    
    # Delete related data
    if quiz_session_ids:
        db.query(UserResponse).filter(UserResponse.quiz_session_id.in_(quiz_session_ids)).delete(synchronize_session=False)
    
    db.query(QuizAttemptHistory).filter(QuizAttemptHistory.user_id == user_id).delete(synchronize_session=False)
    db.query(QuizSession).filter(QuizSession.user_id == user_id).delete(synchronize_session=False)
    db.query(ProgressSnapshot).filter(ProgressSnapshot.user_id == user_id).delete(synchronize_session=False)
    db.query(TopicMastery).filter(TopicMastery.user_id == user_id).delete(synchronize_session=False)
    db.query(LearningSession).filter(LearningSession.user_id == user_id).delete(synchronize_session=False)
    
    db.commit()
    logger.info("✓ Cleaned up old data")
    return True


def create_progress_snapshots(db, user_id: int, days: int):
    """Create daily progress snapshots."""
    logger.info(f"Creating {days} days of progress snapshots...")
    
    snapshots_created = 0
    for day in range(days, 0, -1):
        snapshot_date = datetime.utcnow() - timedelta(days=day)
        
        # Simulate improving performance
        progress = (days - day) / days  # 0 to 1
        base_accuracy = 45 + (progress * 35)  # 45% to 80%
        noise = random.uniform(-5, 5)
        overall_accuracy = min(95, max(35, base_accuracy + noise))
        
        ability_score = (overall_accuracy - 20) / 80  # Scale to 0-1
        
        # Difficulty breakdown
        easy_accuracy = min(95, overall_accuracy + 10)
        medium_accuracy = overall_accuracy
        difficult_accuracy = max(30, overall_accuracy - 15)
        
        # Learning time (minutes)
        learning_time = 30 + (day * 5)  # Cumulative
        
        # Question counts
        questions_attempted = 20 + (days - day) * 5
        questions_correct = int(questions_attempted * overall_accuracy / 100)
        
        snapshot = ProgressSnapshot(
            user_id=user_id,
            snapshot_date=snapshot_date,
            snapshot_type="daily",
            overall_accuracy=overall_accuracy,
            ability_score=ability_score,
            total_questions_attempted=questions_attempted,
            total_questions_correct=questions_correct,
            easy_accuracy=easy_accuracy,
            medium_accuracy=medium_accuracy,
            difficult_accuracy=difficult_accuracy,
            total_learning_time_minutes=learning_time,
            competence_level="medium" if ability_score < 0.7 else "difficult"
        )
        db.add(snapshot)
        snapshots_created += 1
    
    db.commit()
    logger.info(f"✓ Created {snapshots_created} progress snapshots")


def create_quiz_history(db, user_id: int, days: int):
    """Create quiz attempt history."""
    logger.info(f"Creating quiz history...")
    
    num_quizzes = max(5, days // 2)  # One quiz every ~2 days
    quizzes_created = 0
    
    for i in range(num_quizzes):
        days_ago = days - (i * (days / num_quizzes))
        attempt_date = datetime.utcnow() - timedelta(days=days_ago)
        
        # Improving scores over time
        progress = i / num_quizzes
        base_score = 45 + (progress * 35)
        noise = random.uniform(-8, 8)
        score = min(95, max(30, base_score + noise))
        
        # Create quiz session first
        quiz_session = QuizSession(
            user_id=user_id,
            session_id=f"quiz_{user_id}_{i}_{int(attempt_date.timestamp())}",
            started_at=attempt_date,
            completed_at=attempt_date + timedelta(minutes=random.randint(15, 45)),
            is_completed=True,
            total_questions=10,
            current_question_number=10,
            ability=base_score / 100,
            final_ability=base_score / 100
        )
        db.add(quiz_session)
        db.flush()  # Get the quiz_session.id
        
        # Create quiz attempt history
        attempt = QuizAttemptHistory(
            user_id=user_id,
            quiz_session_id=quiz_session.id,
            attempted_at=attempt_date,
            score=score,
            total_questions=10,
            correct_answers=int(10 * score / 100),
            easy_correct=random.randint(3, 4),
            easy_total=4,
            medium_correct=random.randint(2, 3),
            medium_total=3,
            difficult_correct=random.randint(0, 2),
            difficult_total=3,
            duration_minutes=random.randint(15, 45),
            quiz_type="practice"
        )
        db.add(attempt)
        quizzes_created += 1
    
    db.commit()
    logger.info(f"✓ Created {quizzes_created} quiz attempts")


def create_topic_mastery(db, user_id: int):
    """Create topic mastery records."""
    logger.info(f"Creating topic mastery data...")
    
    topics = {
        "Probability": {"mastery": 0.85, "correct": 45, "total": 53},
        "Statistics": {"mastery": 0.72, "correct": 38, "total": 53},
        "Combinatorics": {"mastery": 0.65, "correct": 32, "total": 49},
        "Distributions": {"mastery": 0.58, "correct": 28, "total": 48},
        "Conditional Probability": {"mastery": 0.52, "correct": 24, "total": 46},
    }
    
    topics_created = 0
    for topic_name, data in topics.items():
        mastery = TopicMastery(
            user_id=user_id,
            topic=topic_name,
            mastery_level=data["mastery"],
            total_count=data["total"],
            correct_count=data["correct"],
            attempts=data["total"],
            last_attempted=datetime.utcnow() - timedelta(days=random.randint(0, 3)),
            first_attempted=datetime.utcnow() - timedelta(days=14),
            status="mastered" if data["mastery"] > 0.8 else "learning"
        )
        db.add(mastery)
        topics_created += 1
    
    db.commit()
    logger.info(f"✓ Created {topics_created} topic mastery records")


def create_learning_sessions(db, user_id: int, days: int):
    """Create learning session records."""
    logger.info(f"Creating learning sessions...")
    
    num_sessions = days + 5  # Slightly more sessions than days
    sessions_created = 0
    
    for i in range(num_sessions):
        days_ago = random.uniform(0, days)
        session_date = datetime.utcnow() - timedelta(days=days_ago)
        
        duration = random.randint(20, 60)
        questions_attempted = random.randint(5, 15)
        questions_correct = int(questions_attempted * random.uniform(0.6, 0.9))
        
        session = LearningSession(
            user_id=user_id,
            started_at=session_date,
            ended_at=session_date + timedelta(minutes=duration),
            duration_minutes=duration,
            questions_attempted=questions_attempted,
            questions_correct=questions_correct,
            topics_covered=random.sample(
                ["Probability", "Statistics", "Combinatorics", "Distributions", "Conditional Probability"],
                k=random.randint(1, 3)
            ),
            session_type=random.choice(["practice", "quiz", "study"])
        )
        db.add(session)
        sessions_created += 1
    
    db.commit()
    logger.info(f"✓ Created {sessions_created} learning sessions")


def main():
    """Main function."""
    print("\n" + "=" * 80)
    print("📚 POPULATE LEARNING HISTORY")
    print("=" * 80)
    
    # Parse arguments
    if len(sys.argv) < 2:
        print("\n❌ Error: Missing session_id")
        print("\nUsage:")
        print("  python3 populate_learning_history.py <session_id> [days]")
        print("\nExample:")
        print("  python3 populate_learning_history.py user_abc123 14")
        print("\nTo find your session_id:")
        print("  1. Open http://localhost:3000")
        print("  2. Complete onboarding assessment")
        print("  3. Look at the URL - it will contain your session_id")
        print("  4. Or check the browser's localStorage for 'sessionId'")
        sys.exit(1)
    
    session_id = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    
    print(f"\n📋 Configuration:")
    print(f"   Session ID: {session_id}")
    print(f"   Time Period: {days} days")
    print()
    
    # Initialize database
    initialize_database()
    db = SessionLocal()
    
    try:
        # Find user
        user = find_or_create_user(db, session_id)
        if not user:
            sys.exit(1)
        
        # Clean up existing data if needed
        cleanup_existing_data(db, user.id, session_id)
        
        # Create sample data
        print()
        create_progress_snapshots(db, user.id, days)
        create_quiz_history(db, user.id, days)
        create_topic_mastery(db, user.id)
        create_learning_sessions(db, user.id, days)
        
        print()
        print("=" * 80)
        print("✅ SUCCESS - Learning history populated!")
        print("=" * 80)
        print()
        print("📊 Generated Data:")
        print(f"   • {days} days of progress snapshots")
        print(f"   • {max(5, days // 2)} quiz attempts")
        print(f"   • 5 topic mastery records")
        print(f"   • {days + 5} learning sessions")
        print()
        print("🎯 Next Steps:")
        print("   1. Go to http://localhost:3000")
        print("   2. In the chat, send:")
        print('      "Generate my progress report with visualizations"')
        print("   3. See your learning analytics with charts!")
        print()
        print("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
