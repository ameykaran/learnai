from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

from database import get_db, create_tables
from models import User, QuizSession, Question
from adaptive_algorithm import ImprovedAdaptiveQuizAlgorithm
from questions_data import questions_data

app = FastAPI(title="Adaptive Probability Quiz API", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class StartQuizRequest(BaseModel):
    user_name: Optional[str] = None

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: int
    user_answer: str
    time_taken: Optional[int] = None

class QuizResponse(BaseModel):
    session_id: str
    question: Optional[dict] = None
    message: str

@app.on_event("startup")
async def startup_event():
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
        print(f"Populated database with {len(questions_data)} questions")
    else:
        print(f"Database already contains {existing_questions} questions")

    db.close()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Adaptive Probability Quiz API is running"}

@app.options("/quiz/start")
async def options_start_quiz():
    """Handle OPTIONS request for CORS preflight"""
    return {"message": "OK"}

@app.options("/quiz/submit")
async def options_submit_answer():
    """Handle OPTIONS request for CORS preflight"""
    return {"message": "OK"}

@app.post("/quiz/start")
async def start_quiz(request: StartQuizRequest, db: Session = Depends(get_db)):
    """Start a new quiz session"""
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())

        # Create new user
        user = User(session_id=session_id)
        db.add(user)
        db.flush()  # Get the user ID

        # Create new quiz session
        quiz_session = QuizSession(
            user_id=user.id,
            session_id=session_id
        )
        db.add(quiz_session)
        db.commit()

        # Get the first question
        algorithm = ImprovedAdaptiveQuizAlgorithm(db)
        first_question = algorithm.get_next_question(session_id)

        return {
            "session_id": session_id,
            "question": first_question,
            "message": "Quiz started successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to start quiz: {str(e)}")

@app.get("/quiz/{session_id}/question")
async def get_current_question(session_id: str, db: Session = Depends(get_db)):
    """Get the current question for a quiz session"""
    try:
        algorithm = ImprovedAdaptiveQuizAlgorithm(db)
        question = algorithm.get_next_question(session_id)

        if question is None:
            # Check if quiz is completed
            quiz_session = db.query(QuizSession).filter(
                QuizSession.session_id == session_id
            ).first()

            if quiz_session and quiz_session.is_completed:
                results = algorithm.get_quiz_results(session_id)
                return {
                    "session_id": session_id,
                    "question": None,
                    "message": "Quiz completed",
                    "results": results
                }
            else:
                raise HTTPException(status_code=404, detail="Quiz session not found or no more questions available")

        return {
            "session_id": session_id,
            "question": question,
            "message": "Question retrieved successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get question: {str(e)}")

@app.post("/quiz/submit")
async def submit_answer(request: SubmitAnswerRequest, db: Session = Depends(get_db)):
    """Submit an answer for the current question"""
    try:
        algorithm = ImprovedAdaptiveQuizAlgorithm(db)
        result = algorithm.submit_answer(
            request.session_id,
            request.question_id,
            request.user_answer,
            request.time_taken
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        response_data = {
            "session_id": request.session_id,
            "is_correct": result["is_correct"],
            "correct_answer": result["correct_answer"],
            "is_quiz_complete": result["is_quiz_complete"],
            "message": "Answer submitted successfully"
        }

        if result["is_quiz_complete"]:
            # Get final results
            quiz_results = algorithm.get_quiz_results(request.session_id)
            response_data["results"] = quiz_results
            response_data["competence_level"] = result["competence_level"]
        else:
            # Get next question
            next_question = algorithm.get_next_question(request.session_id)
            response_data["next_question"] = next_question

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")

@app.get("/quiz/{session_id}/results")
async def get_quiz_results(session_id: str, db: Session = Depends(get_db)):
    """Get results for a completed quiz session"""
    try:
        algorithm = ImprovedAdaptiveQuizAlgorithm(db)
        results = algorithm.get_quiz_results(session_id)

        if "error" in results:
            raise HTTPException(status_code=404, detail=results["error"])

        return results

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get results: {str(e)}")

@app.delete("/quiz/{session_id}")
async def reset_quiz(session_id: str, db: Session = Depends(get_db)):
    """Reset/delete a quiz session"""
    try:
        # Find and delete quiz session and related data
        quiz_session = db.query(QuizSession).filter(
            QuizSession.session_id == session_id
        ).first()

        if not quiz_session:
            raise HTTPException(status_code=404, detail="Quiz session not found")

        # Delete user responses
        from models import UserResponse
        db.query(UserResponse).filter(
            UserResponse.quiz_session_id == quiz_session.id
        ).delete()

        # Delete quiz session
        db.delete(quiz_session)

        # Delete user
        user = db.query(User).filter(User.id == quiz_session.user_id).first()
        if user:
            db.delete(user)

        db.commit()

        return {"message": "Quiz session reset successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to reset quiz: {str(e)}")

@app.get("/quiz/stats")
async def get_quiz_stats(db: Session = Depends(get_db)):
    """Get overall quiz statistics"""
    try:
        total_questions = db.query(Question).count()
        easy_questions = db.query(Question).filter(Question.difficulty == "easy").count()
        medium_questions = db.query(Question).filter(Question.difficulty == "medium").count()
        difficult_questions = db.query(Question).filter(Question.difficulty == "difficult").count()

        total_sessions = db.query(QuizSession).count()
        completed_sessions = db.query(QuizSession).filter(QuizSession.is_completed == True).count()

        return {
            "total_questions": total_questions,
            "questions_by_difficulty": {
                "easy": easy_questions,
                "medium": medium_questions,
                "difficult": difficult_questions
            },
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)