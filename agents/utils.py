"""Utilities: logging setup and simple caching wrappers.

Provides a standard logging configuration that writes both human-readable
logs to the console and structured JSON lines to a logfile so every action
can be audited and traced.
"""
import logging
import json
from functools import lru_cache, wraps
from typing import Callable
from pathlib import Path
import time
from datetime import datetime


class _JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        dt_object = datetime.fromtimestamp(time.time())
        readable_time = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        payload = {
            "timestamp": readable_time,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # include extra fields if present
        if hasattr(record, "extra_json"):
            payload.update(record.extra_json)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(level=logging.INFO, logfile: str = "logs/agents.jsonl"):
    """Configure root logger with console + JSONL file handlers.

    - logfile: path to the JSONL log file (created if absent).
    """
    # ensure directory exists
    p = Path(logfile)
    p.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)

    # clear existing handlers to avoid duplicates
    for h in list(root.handlers):
        root.removeHandler(h)

    # console handler (human readable)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root.addHandler(ch)

    # jsonl file handler
    fh = logging.FileHandler(p, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(_JsonLineFormatter())
    root.addHandler(fh)


def cached_retrieval(maxsize: int = 1024):
    """Decorator for caching retrieval-like functions (in-memory LRU)."""

    def _decorator(fn: Callable):
        cached = lru_cache(maxsize=maxsize)(fn)

        @wraps(fn)
        def _wrapped(*args, **kwargs):
            return cached(*args, **kwargs)

        # expose clear function
        _wrapped.cache_clear = cached.cache_clear  # type: ignore
        return _wrapped

    return _decorator


__all__ = ["setup_logging", "cached_retrieval"]
