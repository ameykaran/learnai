"""Simple filesystem-backed session manager for conversation state.

This is intentionally lightweight: it stores JSON session blobs under
`.sessions/` inside the project. Replace with S3 or other backend in prod.
"""
import json
from pathlib import Path
from typing import Any, Dict
import json
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
            return {"messages": []}
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            logger.info("session_loaded", extra={"extra_json": {"session_id": session_id, "size": len(str(data))}})
            return data
        except Exception as e:
            logger.exception("failed_loading_session: %s", e)
            return {"messages": []}

    def save_session(self, session_id: str, session: Dict[str, Any]) -> None:
        p = self._path(session_id)
        p.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("session_saved", extra={"extra_json": {"session_id": session_id, "size": len(str(session))}})


__all__ = ["SessionManager"]
