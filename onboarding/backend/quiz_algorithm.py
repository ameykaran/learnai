import random
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from models import Question, QuizSession, UserResponse

class AdaptiveQuizAlgorithm:
    def __init__(self, db: Session):
        self.db = db

    def get_next_question(self, session_id: str) -> Dict:
        """
        Get the next question for the user based on adaptive algorithm
        """
        quiz_session = self.db.query(QuizSession).filter(
            QuizSession.session_id == session_id
        ).first()

        if not quiz_session:
            return None

        if quiz_session.current_question_number > quiz_session.total_questions:
            return None

        # Determine which difficulty level to use
        difficulty = self._determine_difficulty(quiz_session)

        # Get available questions for this difficulty
        used_question_ids = [
            response.question_id for response in quiz_session.user_responses
        ]

        available_questions = self.db.query(Question).filter(
            Question.difficulty == difficulty,
            Question.id.notin_(used_question_ids)
        ).all()

        if not available_questions:
            # If no questions available in current difficulty, try other difficulties
            all_available_questions = self.db.query(Question).filter(
                Question.id.notin_(used_question_ids)
            ).all()
            if all_available_questions:
                available_questions = all_available_questions
            else:
                return None

        # Select a random question from available questions
        selected_question = random.choice(available_questions)

        return {
            "id": selected_question.id,
            "question_text": selected_question.question_text,
            "options": {
                "A": selected_question.option_a,
                "B": selected_question.option_b,
                "C": selected_question.option_c,
                "D": selected_question.option_d
            },
            "difficulty": selected_question.difficulty,
            "question_number": quiz_session.current_question_number
        }

    def _determine_difficulty(self, quiz_session: QuizSession) -> str:
        """
        Determine the difficulty level for the next question based on performance
        """
        # For the first 5 questions, always start with easy
        if quiz_session.current_question_number <= 5:
            return "easy"

        # Calculate performance metrics
        easy_accuracy = (quiz_session.easy_correct / quiz_session.easy_total) if quiz_session.easy_total > 0 else 0
        medium_accuracy = (quiz_session.medium_correct / quiz_session.medium_total) if quiz_session.medium_total > 0 else 0

        # Adaptive logic:
        # - If user has answered 5+ easy questions with 80%+ accuracy, move to medium
        # - If user has answered 5+ medium questions with 80%+ accuracy, move to difficult
        # - If user struggles with current level (< 60% accuracy), stay at current level or go down

        if quiz_session.easy_total >= 5 and easy_accuracy >= 0.8:
            if quiz_session.medium_total >= 5 and medium_accuracy >= 0.8:
                return "difficult"
            elif quiz_session.medium_total > 0 and medium_accuracy < 0.6:
                return "easy"  # Go back to easy if struggling with medium
            else:
                return "medium"
        elif quiz_session.easy_total > 0 and easy_accuracy < 0.6:
            return "easy"  # Stay at easy if struggling
        else:
            return "easy"  # Default to easy

    def submit_answer(self, session_id: str, question_id: int, user_answer: str, time_taken: int = None) -> Dict:
        """
        Submit an answer and update the quiz session
        """
        quiz_session = self.db.query(QuizSession).filter(
            QuizSession.session_id == session_id
        ).first()

        if not quiz_session:
            return {"error": "Quiz session not found"}

        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return {"error": "Question not found"}

        is_correct = user_answer.upper() == question.correct_answer

        # Create user response record
        user_response = UserResponse(
            quiz_session_id=quiz_session.id,
            question_id=question_id,
            user_answer=user_answer.upper(),
            is_correct=is_correct,
            question_number=quiz_session.current_question_number,
            time_taken_seconds=time_taken
        )
        self.db.add(user_response)

        # Update quiz session statistics
        if question.difficulty == "easy":
            quiz_session.easy_total += 1
            if is_correct:
                quiz_session.easy_correct += 1
        elif question.difficulty == "medium":
            quiz_session.medium_total += 1
            if is_correct:
                quiz_session.medium_correct += 1
        else:  # difficult
            quiz_session.difficult_total += 1
            if is_correct:
                quiz_session.difficult_correct += 1

        # Move to next question
        quiz_session.current_question_number += 1

        # Check if quiz is complete
        if quiz_session.current_question_number > quiz_session.total_questions:
            quiz_session.is_completed = True
            quiz_session.final_competence_level = self._calculate_final_competence(quiz_session)

        self.db.commit()

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "is_quiz_complete": quiz_session.is_completed,
            "competence_level": quiz_session.final_competence_level if quiz_session.is_completed else None
        }

    def _calculate_final_competence(self, quiz_session: QuizSession) -> str:
        """
        Calculate the final competence level based on overall performance
        """
        total_correct = quiz_session.easy_correct + quiz_session.medium_correct + quiz_session.difficult_correct
        total_questions = quiz_session.total_questions
        overall_accuracy = total_correct / total_questions if total_questions > 0 else 0

        # Calculate weighted score based on difficulty
        weighted_score = (
            quiz_session.easy_correct * 1 +
            quiz_session.medium_correct * 2 +
            quiz_session.difficult_correct * 3
        ) / (
            quiz_session.easy_total * 1 +
            quiz_session.medium_total * 2 +
            quiz_session.difficult_total * 3
        ) if (quiz_session.easy_total + quiz_session.medium_total + quiz_session.difficult_total) > 0 else 0

        # Determine competence level
        if weighted_score >= 0.8 and quiz_session.difficult_correct >= 3:
            return "difficult"
        elif weighted_score >= 0.65 and quiz_session.medium_correct >= 5:
            return "medium"
        else:
            return "easy"

    def get_quiz_results(self, session_id: str) -> Dict:
        """
        Get detailed quiz results
        """
        quiz_session = self.db.query(QuizSession).filter(
            QuizSession.session_id == session_id
        ).first()

        if not quiz_session:
            return {"error": "Quiz session not found"}

        total_correct = quiz_session.easy_correct + quiz_session.medium_correct + quiz_session.difficult_correct
        total_questions = quiz_session.total_questions

        return {
            "session_id": session_id,
            "total_questions": total_questions,
            "total_correct": total_correct,
            "overall_accuracy": total_correct / total_questions if total_questions > 0 else 0,
            "easy_stats": {
                "correct": quiz_session.easy_correct,
                "total": quiz_session.easy_total,
                "accuracy": quiz_session.easy_correct / quiz_session.easy_total if quiz_session.easy_total > 0 else 0
            },
            "medium_stats": {
                "correct": quiz_session.medium_correct,
                "total": quiz_session.medium_total,
                "accuracy": quiz_session.medium_correct / quiz_session.medium_total if quiz_session.medium_total > 0 else 0
            },
            "difficult_stats": {
                "correct": quiz_session.difficult_correct,
                "total": quiz_session.difficult_total,
                "accuracy": quiz_session.difficult_correct / quiz_session.difficult_total if quiz_session.difficult_total > 0 else 0
            },
            "final_competence_level": quiz_session.final_competence_level,
            "is_completed": quiz_session.is_completed
        }