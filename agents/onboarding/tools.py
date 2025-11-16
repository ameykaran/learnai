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
from database.models import QuizSession, User
from database.database import get_db, create_tables
from agents.onboarding.backend.adaptive_algorithm import ImprovedAdaptiveQuizAlgorithm
from shared.models import UserProfile

# Import prompts
from agents.onboarding.prompts import (
    USER_GREETING,
    COMPLETION_MESSAGE,
    get_question_prompt,
    get_feedback_prompt,
    get_results_prompt
)


class OnboardingTools:
    """
    Collection of tools for the onboarding agent.
    These tools provide access to the adaptive quiz functionality.
    """
    
    def __init__(self):
        """Initialize tools with database connection."""
        create_tables()  # Ensure tables exist
        self.current_session = None
        self.last_profile = None  # Store the last generated profile for retrieval
        self.profile_callback = None  # Optional callback for profile storage
        self.websocket_callback = None  # Optional callback for sending intermediate messages
    
    def set_websocket_callback(self, callback):
        """
        Set a callback function to send intermediate messages via WebSocket.
        The callback should accept a message string and can be sync or async.
        """
        self.websocket_callback = callback
    
    def _send_websocket_message(self, message: str):
        """Send a message via WebSocket if callback is set."""
        if self.websocket_callback:
            try:
                import asyncio
                import inspect
                
                # Check if callback is async
                if inspect.iscoroutinefunction(self.websocket_callback):
                    # Create task in event loop
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            # If loop is running, create task
                            asyncio.create_task(self.websocket_callback(message))
                        else:
                            # If no loop, run it
                            loop.run_until_complete(self.websocket_callback(message))
                    except RuntimeError:
                        # No event loop, create new one
                        asyncio.run(self.websocket_callback(message))
                else:
                    # Sync callback
                    self.websocket_callback(message)
                    
                print(f"✅ Sent WebSocket message: {message[:100]}...")
            except Exception as e:
                print(f"⚠️  WebSocket callback failed: {e}")
                import traceback
                traceback.print_exc()
    
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
                'started_at': datetime.now()
            }
            
            db.close()
            
            # Format greeting message
            greeting = USER_GREETING.format(total_questions=quiz_session.total_questions)
            
            # Send greeting immediately via WebSocket
            print(f"🚀 Attempting to send greeting via WebSocket...")
            self._send_websocket_message(greeting)
            print(f"✅ Greeting sent successfully")
            
            return {
                "status": "success",
                "session_id": session_id,
                "user_id": user_id,
                "total_questions": quiz_session.total_questions,
                "greeting": greeting,
                "message": f"Assessment ready with {quiz_session.total_questions} questions.",
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
                        "message": COMPLETION_MESSAGE
                    }
                else:
                    db.close()
                    return {
                        "status": "error",
                        "message": "No more questions available or session not found."
                    }
            
            # Get quiz session to determine question number
            quiz_session = db.query(QuizSession).filter(
                QuizSession.session_id == session_id
            ).first()
            
            question_num = quiz_session.current_question_number if quiz_session else 1
            total_questions = quiz_session.total_questions if quiz_session else 25
            
            # Format question using prompt template
            formatted_question = get_question_prompt(
                question=question,
                question_num=question_num,
                total=total_questions
            )
            
            # Send question immediately via WebSocket
            self._send_websocket_message(formatted_question)
            
            db.close()
            
            return {
                "status": "success",
                "question": question,
                "formatted_question": formatted_question,
                "question_number": question_num,
                "total_questions": total_questions
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
            
            # Get question explanation if available
            explanation = result.get("explanation", None)
            
            # Format feedback using prompt template
            feedback = get_feedback_prompt(
                is_correct=result["is_correct"],
                correct_answer=result["correct_answer"],
                explanation=explanation
            )
            
            # Send feedback immediately via WebSocket
            self._send_websocket_message(feedback)
            
            # Prepare response
            response = {
                "status": "success",
                "is_correct": result["is_correct"],
                "correct_answer": result["correct_answer"],
                "is_quiz_complete": result["is_quiz_complete"],
                "feedback": feedback
            }
            
            # If quiz is complete, indicate next step
            if result["is_quiz_complete"]:
                completion_msg = COMPLETION_MESSAGE
                self._send_websocket_message(completion_msg)
                response["message"] = completion_msg
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
            
            # Store profile for retrieval
            self.last_profile = user_profile
            
            # Call callback if registered (for orchestrator to capture profile)
            if self.profile_callback:
                try:
                    self.profile_callback(user_id, user_profile)
                except Exception as e:
                    print(f"Warning: Profile callback failed: {e}")
            
            # Get profile summary and format with results prompt
            profile_summary = user_profile.get_summary()
            formatted_results = get_results_prompt(profile_summary)
            
            # Send results immediately via WebSocket
            self._send_websocket_message(formatted_results)
            
            db.close()
            
            return {
                "status": "success",
                "message": formatted_results,
                "user_profile": user_profile.to_dict(),
                "summary": profile_summary
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to finalize assessment: {str(e)}"
            }
    
    def get_last_profile(self) -> Optional[UserProfile]:
        """
        Get the last generated profile.
        Used by orchestrator to retrieve profile after finalization.
        """
        return self.last_profile
    
    def set_profile_callback(self, callback):
        """
        Set a callback function to be called when a profile is generated.
        The callback should accept (user_id: str, profile: UserProfile).
        """
        self.profile_callback = callback
    
    def clear_profile(self):
        """Clear the stored profile."""
        self.last_profile = None


# Create instance for easy import
onboarding_tools = OnboardingTools()

# Export individual tool functions for agent
start_assessment = onboarding_tools.start_assessment
get_next_question = onboarding_tools.get_next_question
submit_answer = onboarding_tools.submit_answer
get_progress = onboarding_tools.get_progress
finalize_assessment = onboarding_tools.finalize_assessment
