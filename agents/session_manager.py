"""Simple filesystem-backed session manager for conversation state.

This is intentionally lightweight: it stores JSON session blobs under
`.sessions/` inside the project. Replace with S3 or other backend in prod.

Enhanced with time-series data storage for progress tracking.
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

SESSIONS_DIR = Path(".sessions")
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


class SessionManager:
    def __init__(self, base_dir: Path = SESSIONS_DIR):
        self.base_dir = base_dir

    def _path(self, session_id: str) -> Path:
        return self.base_dir / f"{session_id}.json"

    def load_session(self, session_id: str) -> Dict[str, Any]:
        p = self._path(session_id)
        logger.info("load_session", extra={"extra_json": {"session_id": session_id, "path": str(p)}})
        if not p.exists():
            logger.info("session_not_found", extra={"extra_json": {"session_id": session_id}})
            return self._create_new_session()
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            logger.info("session_loaded", extra={"extra_json": {"session_id": session_id, "size": len(str(data))}})
            return data
        except Exception as e:
            logger.exception("failed_loading_session: %s", e)
            return self._create_new_session()

    def save_session(self, session_id: str, session: Dict[str, Any]) -> None:
        """Save session data with automatic timestamping."""
        # Add timestamp for last update
        session['last_updated'] = datetime.now().isoformat()
        
        p = self._path(session_id)
        p.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("session_saved", extra={"extra_json": {"session_id": session_id, "size": len(str(session))}})
    
    def _create_new_session(self) -> Dict[str, Any]:
        """Create a new session with default structure."""
        return {
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "progress_history": [],  # Time-series progress data
            "quiz_history": [],  # Historical quiz attempts
            "activity_log": []  # Learning activity log
        }
    
    def add_progress_snapshot(
        self,
        session_id: str,
        snapshot_data: Dict[str, Any]
    ) -> None:
        """
        Add a progress snapshot to the session.
        
        Args:
            session_id: Session identifier
            snapshot_data: Progress snapshot dictionary
        """
        session = self.load_session(session_id)
        
        if 'progress_history' not in session:
            session['progress_history'] = []
        
        # Add timestamp if not present
        if 'timestamp' not in snapshot_data:
            snapshot_data['timestamp'] = datetime.now().isoformat()
        
        session['progress_history'].append(snapshot_data)
        
        # Keep only last N snapshots to avoid bloat (e.g., last 100)
        if len(session['progress_history']) > 100:
            session['progress_history'] = session['progress_history'][-100:]
        
        self.save_session(session_id, session)
        logger.info(
            "progress_snapshot_added",
            extra={"extra_json": {"session_id": session_id, "total_snapshots": len(session['progress_history'])}}
        )
    
    def add_quiz_attempt(
        self,
        session_id: str,
        quiz_data: Dict[str, Any]
    ) -> None:
        """
        Record a quiz attempt in the session.
        
        Args:
            session_id: Session identifier
            quiz_data: Quiz attempt data
        """
        session = self.load_session(session_id)
        
        if 'quiz_history' not in session:
            session['quiz_history'] = []
        
        # Add timestamp if not present
        if 'timestamp' not in quiz_data:
            quiz_data['timestamp'] = datetime.now().isoformat()
        
        session['quiz_history'].append(quiz_data)
        
        # Keep only last N attempts
        if len(session['quiz_history']) > 50:
            session['quiz_history'] = session['quiz_history'][-50:]
        
        self.save_session(session_id, session)
        logger.info(
            "quiz_attempt_added",
            extra={"extra_json": {"session_id": session_id, "total_quizzes": len(session['quiz_history'])}}
        )
    
    def log_activity(
        self,
        session_id: str,
        activity_type: str,
        activity_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a learning activity.
        
        Args:
            session_id: Session identifier
            activity_type: Type of activity (quiz, study, practice, etc.)
            activity_data: Additional activity data
        """
        session = self.load_session(session_id)
        
        if 'activity_log' not in session:
            session['activity_log'] = []
        
        activity_entry = {
            'type': activity_type,
            'timestamp': datetime.now().isoformat(),
            'data': activity_data or {}
        }
        
        session['activity_log'].append(activity_entry)
        
        # Keep only last N activities
        if len(session['activity_log']) > 200:
            session['activity_log'] = session['activity_log'][-200:]
        
        self.save_session(session_id, session)
        logger.info(
            "activity_logged",
            extra={"extra_json": {"session_id": session_id, "activity_type": activity_type}}
        )
    
    def get_progress_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> list:
        """
        Get progress history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of snapshots to return
            
        Returns:
            List of progress snapshots
        """
        session = self.load_session(session_id)
        history = session.get('progress_history', [])
        
        if limit:
            return history[-limit:]
        return history
    
    def get_quiz_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> list:
        """
        Get quiz history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of attempts to return
            
        Returns:
            List of quiz attempts
        """
        session = self.load_session(session_id)
        history = session.get('quiz_history', [])
        
        if limit:
            return history[-limit:]
        return history
    
    def get_activity_log(
        self,
        session_id: str,
        activity_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> list:
        """
        Get activity log for a session.
        
        Args:
            session_id: Session identifier
            activity_type: Filter by activity type
            limit: Maximum number of activities to return
            
        Returns:
            List of activities
        """
        session = self.load_session(session_id)
        activities = session.get('activity_log', [])
        
        if activity_type:
            activities = [a for a in activities if a.get('type') == activity_type]
        
        if limit:
            return activities[-limit:]
        return activities


__all__ = ["SessionManager"]

