"""
Backend utilities for report generation and time-series analysis.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import asdict
import statistics
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from database.models import (
    User, QuizSession, UserResponse, 
    ProgressSnapshot, QuizAttemptHistory, TopicMastery, LearningSession
)
from shared.models import (
    ProgressSnapshot as ProgressSnapshotModel,
    QuizAttempt,
    TopicMasteryRecord,
    LearningReport
)


class ProgressAnalyzer:
    """
    Analyzes student progress and generates insights from time-series data.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_progress_snapshots(
        self, 
        user_id: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        snapshot_type: Optional[str] = None
    ) -> List[ProgressSnapshotModel]:
        """
        Retrieve progress snapshots for a user within a date range.
        
        Args:
            user_id: User ID
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            snapshot_type: Filter by type (daily, weekly, monthly)
            
        Returns:
            List of ProgressSnapshot models
        """
        query = self.db.query(ProgressSnapshot).filter(ProgressSnapshot.user_id == user_id)
        
        if start_date:
            query = query.filter(ProgressSnapshot.snapshot_date >= start_date)
        if end_date:
            query = query.filter(ProgressSnapshot.snapshot_date <= end_date)
        if snapshot_type:
            query = query.filter(ProgressSnapshot.snapshot_type == snapshot_type)
        
        snapshots = query.order_by(ProgressSnapshot.snapshot_date).all()
        
        # Convert to model objects
        return [self._snapshot_to_model(s) for s in snapshots]
    
    def _snapshot_to_model(self, snapshot: ProgressSnapshot) -> ProgressSnapshotModel:
        """Convert DB snapshot to model."""
        return ProgressSnapshotModel(
            user_id=str(snapshot.user_id),
            timestamp=snapshot.snapshot_date,
            overall_accuracy=snapshot.overall_accuracy,
            ability_score=snapshot.ability_score,
            competence_level=snapshot.competence_level or "medium",
            easy_accuracy=snapshot.easy_accuracy,
            medium_accuracy=snapshot.medium_accuracy,
            difficult_accuracy=snapshot.difficult_accuracy,
            total_questions_attempted=snapshot.total_questions_attempted,
            total_questions_correct=snapshot.total_questions_correct,
            topic_scores=snapshot.topic_scores or {},
            learning_time_minutes=snapshot.total_learning_time_minutes,
            quiz_attempts_count=snapshot.quiz_attempts_count,
            snapshot_type=snapshot.snapshot_type
        )
    
    def get_quiz_history(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        quiz_type: Optional[str] = None
    ) -> List[QuizAttempt]:
        """
        Retrieve quiz attempt history for a user.
        """
        query = self.db.query(QuizAttemptHistory).filter(QuizAttemptHistory.user_id == user_id)
        
        if start_date:
            query = query.filter(QuizAttemptHistory.attempted_at >= start_date)
        if end_date:
            query = query.filter(QuizAttemptHistory.attempted_at <= end_date)
        if quiz_type:
            query = query.filter(QuizAttemptHistory.quiz_type == quiz_type)
        
        attempts = query.order_by(QuizAttemptHistory.attempted_at).all()
        
        return [self._attempt_to_model(a) for a in attempts]
    
    def _attempt_to_model(self, attempt: QuizAttemptHistory) -> QuizAttempt:
        """Convert DB attempt to model."""
        return QuizAttempt(
            user_id=str(attempt.user_id),
            quiz_session_id=str(attempt.quiz_session_id),
            attempted_at=attempt.attempted_at,
            score=attempt.score,
            total_questions=attempt.total_questions,
            correct_answers=attempt.correct_answers,
            easy_correct=attempt.easy_correct,
            easy_total=attempt.easy_total,
            medium_correct=attempt.medium_correct,
            medium_total=attempt.medium_total,
            difficult_correct=attempt.difficult_correct,
            difficult_total=attempt.difficult_total,
            topics=attempt.topics or [],
            topic_scores=attempt.topic_scores or {},
            duration_minutes=attempt.duration_minutes,
            quiz_type=attempt.quiz_type
        )
    
    def get_topic_mastery(
        self,
        user_id: int,
        topics: Optional[List[str]] = None
    ) -> Dict[str, TopicMasteryRecord]:
        """
        Retrieve topic mastery records for a user.
        """
        query = self.db.query(TopicMastery).filter(TopicMastery.user_id == user_id)
        
        if topics:
            query = query.filter(TopicMastery.topic.in_(topics))
        
        records = query.all()
        
        return {
            record.topic: self._mastery_to_model(record)
            for record in records
        }
    
    def _mastery_to_model(self, record: TopicMastery) -> TopicMasteryRecord:
        """Convert DB mastery record to model."""
        return TopicMasteryRecord(
            user_id=str(record.user_id),
            topic=record.topic,
            mastery_level=record.mastery_level,
            confidence_score=record.confidence_score,
            attempts=record.attempts,
            correct_count=record.correct_count,
            total_count=record.total_count,
            first_attempted=record.first_attempted,
            last_attempted=record.last_attempted,
            mastery_history=record.mastery_history or [],
            status=record.status
        )
    
    def calculate_improvement_rate(
        self,
        snapshots: List[ProgressSnapshotModel]
    ) -> float:
        """
        Calculate improvement rate as percentage change from first to last snapshot.
        """
        if len(snapshots) < 2:
            return 0.0
        
        first_accuracy = snapshots[0].overall_accuracy
        last_accuracy = snapshots[-1].overall_accuracy
        
        if first_accuracy == 0:
            return 0.0
        
        return ((last_accuracy - first_accuracy) / first_accuracy) * 100
    
    def determine_progress_trend(
        self,
        snapshots: List[ProgressSnapshotModel]
    ) -> str:
        """
        Determine overall progress trend: improving, declining, or stable.
        """
        if len(snapshots) < 2:
            return "stable"
        
        improvement_rate = self.calculate_improvement_rate(snapshots)
        
        if improvement_rate > 5:  # 5% improvement
            return "improving"
        elif improvement_rate < -5:  # 5% decline
            return "declining"
        else:
            return "stable"
    
    def calculate_consistency_score(
        self,
        snapshots: List[ProgressSnapshotModel]
    ) -> float:
        """
        Calculate consistency score (0-1) based on standard deviation of performance.
        Lower variance = higher consistency.
        """
        if len(snapshots) < 2:
            return 1.0
        
        accuracies = [s.overall_accuracy for s in snapshots]
        
        try:
            std_dev = statistics.stdev(accuracies)
            # Normalize: lower std_dev = higher consistency
            # Assuming max std_dev of 30 (highly variable)
            consistency = max(0, 1 - (std_dev / 30))
            return consistency
        except:
            return 1.0
    
    def identify_strongest_topics(
        self,
        topic_mastery: Dict[str, TopicMasteryRecord],
        count: int = 3
    ) -> List[str]:
        """
        Identify the strongest topics based on mastery level.
        """
        sorted_topics = sorted(
            topic_mastery.items(),
            key=lambda x: (x[1].mastery_level, x[1].get_accuracy()),
            reverse=True
        )
        
        return [topic for topic, _ in sorted_topics[:count]]
    
    def identify_weakest_topics(
        self,
        topic_mastery: Dict[str, TopicMasteryRecord],
        count: int = 3,
        threshold: float = 0.60
    ) -> List[str]:
        """
        Identify topics that need improvement (below threshold).
        """
        weak_topics = [
            (topic, record) 
            for topic, record in topic_mastery.items()
            if record.get_accuracy() < threshold * 100
        ]
        
        sorted_weak = sorted(
            weak_topics,
            key=lambda x: x[1].get_accuracy()
        )
        
        return [topic for topic, _ in sorted_weak[:count]]
    
    def identify_mastered_topics(
        self,
        topic_mastery: Dict[str, TopicMasteryRecord],
        threshold: float = 0.80
    ) -> List[str]:
        """
        Identify topics that have been mastered (above threshold).
        """
        return [
            topic for topic, record in topic_mastery.items()
            if record.mastery_level >= threshold and record.status == "mastered"
        ]
    
    def calculate_total_learning_time(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """
        Calculate total learning time in minutes.
        """
        query = self.db.query(
            func.sum(LearningSession.duration_minutes)
        ).filter(LearningSession.user_id == user_id)
        
        if start_date:
            query = query.filter(LearningSession.started_at >= start_date)
        if end_date:
            query = query.filter(LearningSession.started_at <= end_date)
        
        result = query.scalar()
        return result or 0.0
    
    def generate_recommendations(
        self,
        weak_topics: List[str],
        mastered_topics: List[str],
        progress_trend: str,
        consistency_score: float
    ) -> List[str]:
        """
        Generate personalized recommendations based on performance data.
        """
        recommendations = []
        
        # Topic-specific recommendations
        if weak_topics:
            recommendations.append(
                f"Focus on strengthening: {', '.join(weak_topics[:3])}. "
                "Consider reviewing fundamentals and practicing with easier questions first."
            )
        
        # Trend-based recommendations
        if progress_trend == "declining":
            recommendations.append(
                "Your recent performance shows a decline. Take a short break, "
                "review previous topics, and ensure you're not rushing through material."
            )
        elif progress_trend == "improving":
            recommendations.append(
                "Great progress! Keep up the momentum by challenging yourself "
                "with more advanced problems in your strong areas."
            )
        
        # Consistency recommendations
        if consistency_score < 0.6:
            recommendations.append(
                "Your performance varies significantly. Try to establish a "
                "regular study schedule for more consistent learning."
            )
        
        # Mastery-based recommendations
        if mastered_topics:
            recommendations.append(
                f"Excellent mastery of: {', '.join(mastered_topics[:3])}. "
                "Consider helping peers or tackling more advanced applications."
            )
        
        # General recommendations
        if not weak_topics and mastered_topics:
            recommendations.append(
                "You're doing great! Consider exploring related topics or "
                "real-world applications of probability."
            )
        
        return recommendations


def create_learning_report(
    db: Session,
    user_id: int,
    period_days: int = 7
) -> LearningReport:
    """
    Generate a comprehensive learning report for a user.
    
    Args:
        db: Database session
        user_id: User ID
        period_days: Number of days to include in report
        
    Returns:
        LearningReport object
    """
    analyzer = ProgressAnalyzer(db)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)
    
    # Gather data
    snapshots = analyzer.get_progress_snapshots(user_id, start_date, end_date)
    quiz_history = analyzer.get_quiz_history(user_id, start_date, end_date)
    topic_mastery = analyzer.get_topic_mastery(user_id)
    learning_time = analyzer.calculate_total_learning_time(user_id, start_date, end_date)
    
    # Calculate metrics
    if snapshots:
        latest_snapshot = snapshots[-1]
        overall_accuracy = latest_snapshot.overall_accuracy
        ability_score = latest_snapshot.ability_score
        easy_accuracy = latest_snapshot.easy_accuracy
        medium_accuracy = latest_snapshot.medium_accuracy
        difficult_accuracy = latest_snapshot.difficult_accuracy
    else:
        overall_accuracy = ability_score = 0.0
        easy_accuracy = medium_accuracy = difficult_accuracy = 0.0
    
    improvement_rate = analyzer.calculate_improvement_rate(snapshots)
    progress_trend = analyzer.determine_progress_trend(snapshots)
    consistency_score = analyzer.calculate_consistency_score(snapshots)
    
    # Topic analysis
    strongest_topics = analyzer.identify_strongest_topics(topic_mastery)
    weakest_topics = analyzer.identify_weakest_topics(topic_mastery)
    mastered_topics = analyzer.identify_mastered_topics(topic_mastery)
    in_progress_topics = [
        topic for topic, record in topic_mastery.items()
        if record.status == "learning"
    ]
    
    # Generate recommendations
    recommendations = analyzer.generate_recommendations(
        weakest_topics, mastered_topics, progress_trend, consistency_score
    )
    
    # Calculate totals
    total_questions = sum(q.total_questions for q in quiz_history)
    total_correct = sum(q.correct_answers for q in quiz_history)
    
    return LearningReport(
        user_id=str(user_id),
        generated_at=datetime.now(),
        period_start=start_date,
        period_end=end_date,
        overall_accuracy=overall_accuracy,
        ability_score=ability_score,
        improvement_rate=improvement_rate,
        total_learning_time_minutes=learning_time,
        total_quizzes_taken=len(quiz_history),
        total_questions_attempted=total_questions,
        total_questions_correct=total_correct,
        easy_accuracy=easy_accuracy,
        medium_accuracy=medium_accuracy,
        difficult_accuracy=difficult_accuracy,
        strongest_topics=strongest_topics,
        weakest_topics=weakest_topics,
        topics_mastered=mastered_topics,
        topics_in_progress=in_progress_topics,
        progress_trend=progress_trend,
        consistency_score=consistency_score,
        recommended_focus_areas=weakest_topics,
        suggested_next_steps=recommendations,
        progress_snapshots=snapshots,
        quiz_history=quiz_history,
        topic_mastery=topic_mastery
    )
