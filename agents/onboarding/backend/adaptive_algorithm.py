import math
import random
import logging
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Question, QuizSession, UserResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging for ability trace debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImprovedAdaptiveQuizAlgorithm:
    """
    Improved adaptive quiz algorithm with ability model, exploration, and quotas.
    """

    # Hyperparameters (modifiable)
    ALPHA = 6.0  # Steepness of logistic function
    LEARNING_RATE = 0.12  # Learning rate for ability updates
    INITIAL_EPSILON = 0.12  # Initial exploration rate
    INITIAL_ABILITY = 0.25  # Starting ability estimate
    MIN_MEDIUM = 4  # Minimum medium questions to attempt
    MIN_DIFFICULT = 2  # Minimum difficult questions to attempt
    TOTAL_QUESTIONS = int(os.getenv('ONBOARDING_TOTAL_QUESTIONS', '25'))  # Total quiz length (configurable via env var)

    # Difficulty score mapping
    DIFFICULTY_SCORES = {
        'easy': 0.20,
        'medium': 0.50,
        'difficult': 0.80
    }

    def __init__(self, db: Session):
        self.db = db

    def sigmoid(self, x: float) -> float:
        """Logistic sigmoid function with overflow protection."""
        return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))

    def expected_probability(self, ability: float, difficulty_score: float) -> float:
        """Calculate expected probability of correct answer using logistic model."""
        return self.sigmoid(self.ALPHA * (ability - difficulty_score))

    def update_ability(self, current_ability: float, outcome: bool, expected_prob: float) -> float:
        """Update ability using gradient ascent on log-likelihood."""
        outcome_val = 1.0 if outcome else 0.0
        new_ability = current_ability + self.LEARNING_RATE * (outcome_val - expected_prob)
        return max(0.0, min(1.0, new_ability))  # Clip to [0,1]

    def get_exploration_epsilon(self, question_count: int) -> float:
        """Calculate decaying exploration rate."""
        return max(0.05, self.INITIAL_EPSILON * (1 - question_count / self.TOTAL_QUESTIONS))

    def get_next_question(self, session_id: str) -> Optional[Dict]:
        """
        Get the next question using improved adaptive algorithm with exploration and quotas.
        """
        quiz_session = self.db.query(QuizSession).filter(
            QuizSession.session_id == session_id
        ).first()

        if not quiz_session:
            logger.error(f"Quiz session {session_id} not found")
            return None

        if quiz_session.current_question_number > quiz_session.total_questions:
            logger.info(f"Quiz {session_id} already complete")
            return None

        # Initialize fields if they don't exist (backwards compatibility)
        if quiz_session.asked_ids is None:
            quiz_session.asked_ids = []
        if quiz_session.history is None:
            quiz_session.history = []
        if quiz_session.ability is None:
            quiz_session.ability = self.INITIAL_ABILITY

        asked_ids = quiz_session.asked_ids or []
        current_ability = quiz_session.ability
        question_count = quiz_session.current_question_number
        medium_seen = quiz_session.medium_seen or 0
        difficult_seen = quiz_session.difficult_seen or 0

        logger.info(f"Session {session_id}: Q{question_count}, ability={current_ability:.3f}, medium_seen={medium_seen}, difficult_seen={difficult_seen}")

        # Calculate remaining questions and quota requirements
        remaining_questions = self.TOTAL_QUESTIONS - question_count + 1
        min_medium_remaining = max(0, self.MIN_MEDIUM - medium_seen)
        min_difficult_remaining = max(0, self.MIN_DIFFICULT - difficult_seen)

        # Check if we need to force quota fulfillment
        force_quota = remaining_questions <= (min_medium_remaining + min_difficult_remaining)

        if force_quota:
            logger.info(f"Session {session_id}: Forcing quota fulfillment - {min_medium_remaining} medium, {min_difficult_remaining} difficult needed")
            if min_difficult_remaining > 0:
                target_difficulty = 'difficult'
            elif min_medium_remaining > 0:
                target_difficulty = 'medium'
            else:
                target_difficulty = self._get_target_difficulty(current_ability)
        else:
            # Use exploration strategy
            epsilon = self.get_exploration_epsilon(question_count - 1)

            if random.random() < epsilon:
                # Exploration: try one level above current ability
                target_difficulty = self._get_exploration_difficulty(current_ability)
                logger.info(f"Session {session_id}: Exploration (ε={epsilon:.3f}) -> {target_difficulty}")
            else:
                # Exploitation: pick difficulty closest to ability
                target_difficulty = self._get_target_difficulty(current_ability)
                logger.info(f"Session {session_id}: Exploitation -> {target_difficulty}")

        # Get candidate questions
        candidates = self._get_candidate_questions(target_difficulty, asked_ids)

        if not candidates:
            # Fallback to any available question
            logger.warning(f"Session {session_id}: No candidates for {target_difficulty}, trying fallback")
            for fallback_difficulty in ['easy', 'medium', 'difficult']:
                candidates = self._get_candidate_questions(fallback_difficulty, asked_ids)
                if candidates:
                    target_difficulty = fallback_difficulty
                    break

        if not candidates:
            logger.error(f"Session {session_id}: No available questions found")
            return None

        # Select random question from candidates
        selected_question = random.choice(candidates)

        # Update session state
        quiz_session.asked_ids = asked_ids + [selected_question.id]
        if target_difficulty == 'medium':
            quiz_session.medium_seen = medium_seen + 1
        elif target_difficulty == 'difficult':
            quiz_session.difficult_seen = difficult_seen + 1

        self.db.commit()

        logger.info(f"Session {session_id}: Selected Q{selected_question.id} ({target_difficulty})")

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

    def _get_target_difficulty(self, ability: float) -> str:
        """Get target difficulty closest to current ability."""
        target_score = min(1.0, ability + 0.05)  # Slight push upward

        distances = {
            difficulty: abs(score - target_score)
            for difficulty, score in self.DIFFICULTY_SCORES.items()
        }

        return min(distances, key=distances.get)

    def _get_exploration_difficulty(self, ability: float) -> str:
        """Get exploration difficulty (one level above current ability)."""
        if ability >= 0.7:
            return 'difficult'  # High ability users explore difficult
        elif ability >= 0.35:
            return 'difficult' if random.random() < 0.7 else 'medium'  # Bias toward difficult
        else:
            return 'medium'  # Low ability users explore medium

    def _get_candidate_questions(self, difficulty: str, asked_ids: List[int], limit: int = 50) -> List[Question]:
        """Get candidate questions for given difficulty, excluding already asked."""
        return self.db.query(Question).filter(
            Question.difficulty == difficulty,
            ~Question.id.in_(asked_ids or [])
        ).order_by(func.random()).limit(limit).all()

    def submit_answer(self, session_id: str, question_id: int, user_answer: str, time_taken: Optional[int] = None) -> Dict:
        """
        Submit answer and update session using improved adaptive algorithm.
        """
        quiz_session = self.db.query(QuizSession).filter(
            QuizSession.session_id == session_id
        ).first()

        if not quiz_session:
            return {"error": "Quiz session not found"}

        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return {"error": "Question not found"}

        # Server-side correctness verification
        is_correct = user_answer.upper() == question.correct_answer

        # Get current state for ability update
        ability_before = quiz_session.ability or self.INITIAL_ABILITY
        difficulty_score = self.DIFFICULTY_SCORES[question.difficulty]
        expected_prob = self.expected_probability(ability_before, difficulty_score)

        # Update ability
        ability_after = self.update_ability(ability_before, is_correct, expected_prob)
        quiz_session.ability = ability_after

        # Log ability trace for debugging
        outcome = 1 if is_correct else 0
        logger.info(f"ABILITY_TRACE Session {session_id}: Q{question.id} ({question.difficulty}) "
                   f"ability_before={ability_before:.3f} expected={expected_prob:.3f} "
                   f"outcome={outcome} ability_after={ability_after:.3f}")

        # Update history
        history = quiz_session.history or []
        history.append({
            'question_id': question_id,
            'difficulty': question.difficulty,
            'correct': is_correct,
            'ability_before': ability_before,
            'ability_after': ability_after
        })
        quiz_session.history = history

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

        # Update legacy statistics for compatibility
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
            quiz_session.final_ability = ability_after
            quiz_session.final_competence_level = self._calculate_final_competence(ability_after)
            quiz_session.completed_at = datetime.now()

        self.db.commit()

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "is_quiz_complete": quiz_session.is_completed,
            "competence_level": quiz_session.final_competence_level if quiz_session.is_completed else None
        }

    def _calculate_final_competence(self, final_ability: float) -> str:
        """Calculate final competence level based on ability score."""
        if final_ability < 0.35:
            return "easy"
        elif final_ability < 0.65:
            return "medium"
        else:
            return "difficult"

    def get_quiz_results(self, session_id: str) -> Dict:
        """Get detailed quiz results including ability score."""
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
            "is_completed": quiz_session.is_completed,
            "final_ability": quiz_session.final_ability  # For debugging
        }