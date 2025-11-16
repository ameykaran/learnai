"""
Tools for the Report Agent.
Provides functions for retrieving and analyzing student progress data.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from strands import tool
import logging

from database.database import SessionLocal
from agents.report.backend.analytics import ProgressAnalyzer, create_learning_report
from agents.report.backend.chart_renderer import ChartRenderer
from shared.models import LearningReport

logger = logging.getLogger(__name__)


class ReportTools:
    """Tools for report generation."""
    
    def __init__(self):
        self.db = None
    
    def get_db(self):
        """Get database session."""
        if self.db is None:
            self.db = SessionLocal()
        return self.db
    
    def get_user_id_from_session(self, session_id: str) -> Optional[int]:
        """Get user ID from session ID."""
        from database.models import User
        db = self.get_db()
        user = db.query(User).filter(User.session_id == session_id).first()
        return user.id if user else None


# Create a singleton instance
report_tools = ReportTools()


@tool
def get_user_progress_history(
    user_session_id: str,
    days: int = 7
) -> str:
    """
    Retrieve a user's progress history over a specified time period.
    
    Args:
        user_session_id: The user's session ID
        days: Number of days to look back (default: 7)
    
    Returns:
        JSON string containing progress snapshots with timestamps, accuracy, and metrics
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session ID {user_session_id}"
        
        analyzer = ProgressAnalyzer(report_tools.get_db())
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        snapshots = analyzer.get_progress_snapshots(user_id, start_date, end_date)
        
        if not snapshots:
            return f"No progress data found for the last {days} days."
        
        result = {
            "period": f"Last {days} days",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "snapshots_count": len(snapshots),
            "snapshots": [s.to_dict() for s in snapshots]
        }
        
        import json
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting progress history: {e}", exc_info=True)
        return f"Error retrieving progress history: {str(e)}"


@tool
def get_quiz_performance_trends(
    user_session_id: str,
    days: int = 30
) -> str:
    """
    Analyze quiz performance trends over time.
    
    Args:
        user_session_id: The user's session ID
        days: Number of days to analyze (default: 30)
    
    Returns:
        JSON string with quiz history, scores, and trend analysis
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session ID {user_session_id}"
        
        analyzer = ProgressAnalyzer(report_tools.get_db())
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        quiz_history = analyzer.get_quiz_history(user_id, start_date, end_date)
        
        if not quiz_history:
            return f"No quiz attempts found in the last {days} days."
        
        # Calculate trends
        scores = [q.score for q in quiz_history]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Improvement calculation
        if len(scores) >= 2:
            first_half_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
            second_half_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
            improvement = second_half_avg - first_half_avg
        else:
            improvement = 0
        
        result = {
            "period": f"Last {days} days",
            "total_quizzes": len(quiz_history),
            "average_score": round(avg_score, 2),
            "improvement": round(improvement, 2),
            "trend": "improving" if improvement > 5 else "declining" if improvement < -5 else "stable",
            "quiz_attempts": [q.to_dict() for q in quiz_history]
        }
        
        import json
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error analyzing quiz trends: {e}", exc_info=True)
        return f"Error analyzing quiz trends: {str(e)}"


@tool
def get_topic_mastery_analysis(
    user_session_id: str
) -> str:
    """
    Get detailed analysis of topic mastery levels.
    
    Args:
        user_session_id: The user's session ID
    
    Returns:
        JSON string with topic mastery data, strengths, and weaknesses
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session ID {user_session_id}"
        
        analyzer = ProgressAnalyzer(report_tools.get_db())
        topic_mastery = analyzer.get_topic_mastery(user_id)
        
        if not topic_mastery:
            return "No topic mastery data available yet."
        
        strongest = analyzer.identify_strongest_topics(topic_mastery, count=5)
        weakest = analyzer.identify_weakest_topics(topic_mastery, count=5)
        mastered = analyzer.identify_mastered_topics(topic_mastery)
        
        result = {
            "total_topics": len(topic_mastery),
            "mastered_topics": mastered,
            "strongest_topics": strongest,
            "weakest_topics": weakest,
            "topic_details": {
                topic: record.to_dict() 
                for topic, record in topic_mastery.items()
            }
        }
        
        import json
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error analyzing topic mastery: {e}", exc_info=True)
        return f"Error analyzing topic mastery: {str(e)}"


@tool
def get_learning_time_stats(
    user_session_id: str,
    days: int = 7
) -> str:
    """
    Get learning time statistics and engagement metrics.
    
    Args:
        user_session_id: The user's session ID
        days: Number of days to analyze (default: 7)
    
    Returns:
        JSON string with learning time, session count, and engagement metrics
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session ID {user_session_id}"
        
        analyzer = ProgressAnalyzer(report_tools.get_db())
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        total_time = analyzer.calculate_total_learning_time(user_id, start_date, end_date)
        
        # Get session count
        from database.models import LearningSession
        db = report_tools.get_db()
        session_count = db.query(LearningSession).filter(
            LearningSession.user_id == user_id,
            LearningSession.started_at >= start_date,
            LearningSession.started_at <= end_date
        ).count()
        
        avg_session_time = total_time / session_count if session_count > 0 else 0
        
        result = {
            "period": f"Last {days} days",
            "total_learning_time_minutes": round(total_time, 2),
            "total_learning_time_hours": round(total_time / 60, 2),
            "session_count": session_count,
            "average_session_minutes": round(avg_session_time, 2),
            "daily_average_minutes": round(total_time / days, 2)
        }
        
        import json
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error calculating learning time: {e}", exc_info=True)
        return f"Error calculating learning time: {str(e)}"


@tool
def generate_comprehensive_report(
    user_session_id: str,
    days: int = 7
) -> str:
    """
    Generate a comprehensive learning progress report.
    
    Args:
        user_session_id: The user's session ID
        days: Number of days to include in report (default: 7)
    
    Returns:
        Formatted string report with all analytics and recommendations
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session ID {user_session_id}"
        
        db = report_tools.get_db()
        report = create_learning_report(db, user_id, period_days=days)
        
        # Return formatted summary
        return report.get_summary()
        
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return f"Error generating comprehensive report: {str(e)}"


@tool
def compare_time_periods(
    user_session_id: str,
    period1_days: int = 7,
    period2_days: int = 14
) -> str:
    """
    Compare performance between two time periods.
    
    Args:
        user_session_id: The user's session ID
        period1_days: Days for recent period (default: 7)
        period2_days: Days for earlier period (default: 14)
    
    Returns:
        JSON string comparing metrics between the two periods
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session ID {user_session_id}"
        
        analyzer = ProgressAnalyzer(report_tools.get_db())
        
        # Recent period
        end_date = datetime.now()
        period1_start = end_date - timedelta(days=period1_days)
        period1_snapshots = analyzer.get_progress_snapshots(user_id, period1_start, end_date)
        
        # Earlier period
        period2_start = end_date - timedelta(days=period2_days)
        period2_end = period1_start
        period2_snapshots = analyzer.get_progress_snapshots(user_id, period2_start, period2_end)
        
        # Calculate averages
        def avg_accuracy(snapshots):
            if not snapshots:
                return 0.0
            return sum(s.overall_accuracy for s in snapshots) / len(snapshots)
        
        period1_avg = avg_accuracy(period1_snapshots)
        period2_avg = avg_accuracy(period2_snapshots)
        change = period1_avg - period2_avg
        
        result = {
            "recent_period": {
                "days": period1_days,
                "average_accuracy": round(period1_avg, 2),
                "data_points": len(period1_snapshots)
            },
            "earlier_period": {
                "days": period2_days - period1_days,
                "average_accuracy": round(period2_avg, 2),
                "data_points": len(period2_snapshots)
            },
            "comparison": {
                "accuracy_change": round(change, 2),
                "percent_change": round((change / period2_avg * 100) if period2_avg > 0 else 0, 2),
                "trend": "improved" if change > 0 else "declined" if change < 0 else "stable"
            }
        }
        
        import json
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error comparing periods: {e}", exc_info=True)
        return f"Error comparing time periods: {str(e)}"


@tool
def generate_progress_visualizations(
    user_session_id: str,
    days: int = 7,
    format: str = "json"
) -> str:
    """
    Generate visualization data for progress charts and graphs.
    
    Args:
        user_session_id: The user's session ID
        days: Number of days to include (default: 7)
        format: Output format - "json" for chart data or "markdown" for text visualization
    
    Returns:
        JSON string with chart data for:
        - Progress over time (line chart)
        - Difficulty breakdown (bar chart)
        - Topic mastery (horizontal bar chart)
        - Quiz performance trend (line chart)
        - Learning time (bar chart)
        - Topic distribution (pie chart)
        - Consistency gauge
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session ID {user_session_id}"
        
        analyzer = ProgressAnalyzer(report_tools.get_db())
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get all data
        snapshots = analyzer.get_progress_snapshots(user_id, start_date, end_date)
        quiz_history = analyzer.get_quiz_history(user_id, start_date, end_date)
        topic_mastery = analyzer.get_topic_mastery(user_id)
        consistency_score = analyzer.calculate_consistency_score(snapshots)
        
        # Convert to dicts
        snapshots_dict = [s.to_dict() for s in snapshots]
        quiz_dict = [q.to_dict() for q in quiz_history]
        topic_dict = {k: v.to_dict() for k, v in topic_mastery.items()}
        
        # Generate all visualizations
        viz_data = generate_all_visualizations(
            snapshots_dict,
            quiz_dict,
            topic_dict,
            consistency_score
        )
        
        if format == "markdown":
            # Format as text visualization
            output = ["\n" + "="*80]
            output.append("PROGRESS VISUALIZATIONS")
            output.append("="*80)
            
            for chart_name, chart_data in viz_data.items():
                output.append(format_chart_data_as_markdown(chart_data))
                output.append("\n" + "-"*80)
            
            return "\n".join(output)
        else:
            # Return JSON
            import json
            return json.dumps(viz_data, indent=2)
        
    except Exception as e:
        logger.error(f"Error generating visualizations: {e}", exc_info=True)
        return f"Error generating visualizations: {str(e)}"


@tool
def render_progress_charts(
    user_session_id: str,
    days: int = 14,
    chart_type: str = "dashboard"
) -> str:
    """
    Render progress charts as PNG images and save them to the generated directory.
    Returns the filename(s) that can be accessed via the API.
    
    Use this tool to create actual visual charts that can be displayed in the frontend.
    
    Args:
        user_session_id: User's session ID
        days: Number of days to include in the analysis (default: 14)
        chart_type: Type of chart to render:
            - "dashboard": Complete dashboard with all charts (recommended)
            - "progress": Just the progress over time chart
            - "all": All charts as separate files
    
    Returns:
        JSON string with chart filenames and URLs
    """
    try:
        user_id = report_tools.get_user_id_from_session(user_session_id)
        if not user_id:
            return f"Error: User not found with session_id: {user_session_id}"
        
        db = report_tools.get_db()
        analyzer = ProgressAnalyzer(db)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Fetch data
        progress_snapshots = analyzer.get_progress_snapshots(user_id, start_date, end_date)
        quiz_history = analyzer.get_quiz_history(user_id, start_date, end_date)
        topic_mastery = analyzer.get_topic_mastery(user_id)
        consistency_score = analyzer.calculate_consistency_score(progress_snapshots)
        
        if not progress_snapshots:
            return "Error: No progress data found for this user."
        
        # Convert to dict format
        snapshots_dict = [
            {
                'timestamp': s.timestamp.isoformat(),
                'overall_accuracy': s.overall_accuracy,
                'ability_score': s.ability_score,
                'easy_accuracy': s.easy_accuracy,
                'medium_accuracy': s.medium_accuracy,
                'difficult_accuracy': s.difficult_accuracy,
                'learning_time_minutes': s.learning_time_minutes
            }
            for s in progress_snapshots
        ]
        
        quiz_dict = [
            {
                'attempted_at': q.attempted_at.isoformat(),
                'score': q.score
            }
            for q in quiz_history
        ]
        
        topic_dict = {
            name: {
                'mastery_level': data.mastery_level,
                'total_count': data.total_count,
                'correct_count': data.correct_count
            }
            for name, data in topic_mastery.items()
        }
        
        # Generate visualization data
        viz_data = generate_all_visualizations(
            snapshots_dict,
            quiz_dict,
            topic_dict,
            consistency_score
        )
        
        # Render charts
        renderer = ChartRenderer()
        import json
        
        if chart_type == "dashboard":
            # Render complete dashboard
            filename = renderer.render_dashboard(viz_data, user_session_id, days)
            result = {
                "chart_type": "dashboard",
                "filename": filename,
                "url": f"/generated/{filename}",
                "charts_included": [
                    "progress_over_time",
                    "difficulty_breakdown",
                    "quiz_performance_trend",
                    "learning_time",
                    "topic_mastery",
                    "topic_distribution"
                ]
            }
            return json.dumps(result, indent=2)
        
        elif chart_type == "all":
            # Render each chart separately
            filenames = {}
            for chart_name, chart_data in viz_data.items():
                if chart_name != "consistency_gauge":  # Skip gauge for now
                    filename = renderer.render_single_chart(
                        chart_data, user_session_id, chart_name
                    )
                    filenames[chart_name] = {
                        "filename": filename,
                        "url": f"/generated/{filename}"
                    }
            
            result = {
                "chart_type": "all",
                "charts": filenames
            }
            return json.dumps(result, indent=2)
        
        else:
            # Render single chart
            if chart_type not in viz_data:
                return f"Error: Unknown chart type: {chart_type}"
            
            filename = renderer.render_single_chart(
                viz_data[chart_type], user_session_id, chart_type
            )
            result = {
                "chart_type": chart_type,
                "filename": filename,
                "url": f"/generated/{filename}"
            }
            return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error rendering charts: {e}", exc_info=True)
        return f"Error rendering charts: {str(e)}"


# Export all tools
report_agent_tools = [
    get_user_progress_history,
    get_quiz_performance_trends,
    get_topic_mastery_analysis,
    get_learning_time_stats,
    generate_comprehensive_report,
    compare_time_periods,
    generate_progress_visualizations,
    render_progress_charts
]
