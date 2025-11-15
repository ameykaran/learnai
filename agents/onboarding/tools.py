"""
Onboarding Agent Tools - Strands tools for adaptive assessment.
These tools wrap the existing adaptive quiz logic.
"""

import sys
import os
from pathlib import Path

# Add the onboarding backend to Python path
backend_path = Path(__file__).parent.parent.parent / "onboarding" / "backend"
sys.path.insert(0, str(backend_path))

from typing import Optional, Dict
from strands import tool
from datetime import datetime
import uuid

# Import existing backend components
from database import get_db, create_tables
from models import QuizSession, User
from adaptive_algorithm import ImprovedAdaptiveQuizAlgorithm
from shared.models import UserProfile


class OnboardingTools:
    """
    Collection of tools for the onboarding agent.
    These tools provide access to the adaptive quiz functionality.
    """
    
    def __init__(self):
        """Initialize tools with database connection."""
        create_tables()  # Ensure tables exist
        self.current_session = None
    
    @tool
    def start_assessment(self, user_id: str, total_questions: Optional[int] = None) -> dict:
        """
        Initialize a new adaptive assessment for a user.
        
        This tool starts a probability knowledge assessment that adapts
        to the user's ability level. It creates a quiz session and prepares
        the first question.
        
        Args:
            user_id: Unique identifier for the user
            total_questions: Optional override for number of questions (default from env)
        
        Returns:
            Dictionary containing session_id, first question, and assessment info
        """
        try:
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            
            # Get database session
            db = next(get_db())
            
            # Create user record
            user = User(session_id=session_id)
            db.add(user)
            db.flush()
            
            # Create quiz session
            quiz_session = QuizSession(
                user_id=user.id,
                session_id=session_id
            )
            
            # Override total_questions if provided
            if total_questions:
                quiz_session.total_questions = total_questions
            
            db.add(quiz_session)
            db.commit()
            
            # Get first question using adaptive algorithm
            algorithm = ImprovedAdaptiveQuizAlgorithm(db)
            first_question = algorithm.get_next_question(session_id)
            
            # Store session info for later use
            self.current_session = {
                'session_id': session_id,
                'user_id': user_id,
                'total_questions': quiz_session.total_questions,
                'started_at': datetime.utcnow()
            }
            
            db.close()
            
            return {
                "status": "success",
                "session_id": session_id,
                "user_id": user_id,
                "total_questions": quiz_session.total_questions,
                "message": f"Assessment started! You will answer {quiz_session.total_questions} adaptive questions.",
                "first_question": first_question
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to start assessment: {str(e)}"
            }
    
    @tool
    def get_next_question(self, session_id: str) -> dict:
        """
        Get the next question in the adaptive assessment.
        
        The question difficulty adapts based on the user's performance
        on previous questions.
        
        Args:
            session_id: The quiz session identifier
        
        Returns:
            Dictionary containing the next question with options and metadata
        """
        try:
            db = next(get_db())
            algorithm = ImprovedAdaptiveQuizAlgorithm(db)
            
            question = algorithm.get_next_question(session_id)
            
            if question is None:
                # Check if quiz is complete
                quiz_session = db.query(QuizSession).filter(
                    QuizSession.session_id == session_id
                ).first()
                
                if quiz_session and quiz_session.is_completed:
                    db.close()
                    return {
                        "status": "completed",
                        "message": "Assessment complete! Use finalize_assessment to get results."
                    }
                else:
                    db.close()
                    return {
                        "status": "error",
                        "message": "No more questions available or session not found."
                    }
            
            db.close()
            
            return {
                "status": "success",
                "question": question
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get question: {str(e)}"
            }
    
    @tool
    def submit_answer(self, session_id: str, question_id: int, user_answer: str) -> dict:
        """
        Submit an answer to a question and get immediate feedback.
        
        This tool processes the user's answer, updates their ability estimate,
        and provides feedback on correctness.
        
        Args:
            session_id: The quiz session identifier
            question_id: The ID of the question being answered
            user_answer: The user's selected answer (A, B, C, or D)
        
        Returns:
            Dictionary with correctness, correct answer, and next steps
        """
        try:
            db = next(get_db())
            algorithm = ImprovedAdaptiveQuizAlgorithm(db)
            
            # Submit answer and get result
            result = algorithm.submit_answer(
                session_id=session_id,
                question_id=question_id,
                user_answer=user_answer.upper(),
                time_taken=None
            )
            
            if "error" in result:
                db.close()
                return {
                    "status": "error",
                    "message": result["error"]
                }
            
            # Prepare response
            response = {
                "status": "success",
                "is_correct": result["is_correct"],
                "correct_answer": result["correct_answer"],
                "is_quiz_complete": result["is_quiz_complete"]
            }
            
            # Add feedback message
            if result["is_correct"]:
                response["feedback"] = "✓ Correct! Well done."
            else:
                response["feedback"] = f"✗ Incorrect. The correct answer was {result['correct_answer']}."
            
            # If quiz is complete, indicate next step
            if result["is_quiz_complete"]:
                response["message"] = "Assessment complete! Use finalize_assessment to generate your profile."
                response["competence_level"] = result.get("competence_level")
            
            db.close()
            
            return response
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to submit answer: {str(e)}"
            }
    
    @tool
    def get_progress(self, session_id: str) -> dict:
        """
        Check the current progress of the assessment.
        
        Args:
            session_id: The quiz session identifier
        
        Returns:
            Dictionary with progress information
        """
        try:
            db = next(get_db())
            
            quiz_session = db.query(QuizSession).filter(
                QuizSession.session_id == session_id
            ).first()
            
            if not quiz_session:
                db.close()
                return {
                    "status": "error",
                    "message": "Session not found"
                }
            
            questions_answered = quiz_session.current_question_number - 1
            total_questions = quiz_session.total_questions
            
            db.close()
            
            return {
                "status": "success",
                "questions_answered": questions_answered,
                "total_questions": total_questions,
                "questions_remaining": total_questions - questions_answered,
                "is_complete": quiz_session.is_completed,
                "current_ability": quiz_session.ability
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get progress: {str(e)}"
            }
    
    @tool
    def finalize_assessment(self, session_id: str, user_id: str) -> dict:
        """
        Finalize the assessment and generate user profile.
        
        This tool should be called when the assessment is complete.
        It generates a comprehensive UserProfile that will be stored
        in the orchestrator's memory.
        
        Args:
            session_id: The quiz session identifier
            user_id: The user identifier
        
        Returns:
            Dictionary containing the UserProfile and summary
        """
        try:
            db = next(get_db())
            algorithm = ImprovedAdaptiveQuizAlgorithm(db)
            
            # Get quiz results
            quiz_results = algorithm.get_quiz_results(session_id)
            
            if "error" in quiz_results:
                db.close()
                return {
                    "status": "error",
                    "message": quiz_results["error"]
                }
            
            # Check if quiz is actually completed
            if not quiz_results.get("is_completed", False):
                db.close()
                return {
                    "status": "error",
                    "message": "Assessment is not yet complete. Please answer all questions first."
                }
            
            # Create UserProfile from quiz results
            user_profile = UserProfile.from_quiz_results(
                quiz_results=quiz_results,
                user_id=user_id,
                session_id=session_id
            )
            
            db.close()
            
            return {
                "status": "success",
                "message": "Assessment finalized successfully!",
                "user_profile": user_profile.to_dict(),
                "summary": user_profile.get_summary()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to finalize assessment: {str(e)}"
            }


# Create instance for easy import
onboarding_tools = OnboardingTools()

# Export individual tool functions for agent
start_assessment = onboarding_tools.start_assessment
get_next_question = onboarding_tools.get_next_question
submit_answer = onboarding_tools.submit_answer
get_progress = onboarding_tools.get_progress
finalize_assessment = onboarding_tools.finalize_assessment
