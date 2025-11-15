import logging
import warnings
from logging import Logger
import sys

COLORS = {
    "DEBUG": "\033[36m",   # Cyan
    "INFO": "\033[32m",    # Green
    "WARNING": "\033[33m", # Yellow
    "ERROR": "\033[31m",   # Red
    "CRITICAL": "\033[41m" # Red background
}
RESET = "\033[0m"

class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, RESET)
        record.levelname = f"{color}{record.levelname}{RESET}"
        return super().format(record)


def configure_logging(level=logging.INFO, debug_mode=False):
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (default: INFO)
        debug_mode: If True, show all debug logs including from libraries
    """
    fmt = (
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(module)s:%(funcName)s:%(lineno)d | %(message)s"
    )
    formatter = ColorFormatter(fmt)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]
    
    # Suppress specific warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='strands.agent.agent')
    
    # if not debug_mode:
    #     # Set specific loggers to less verbose levels
    #     logging.getLogger('botocore').setLevel(logging.WARNING)
    #     logging.getLogger('urllib3').setLevel(logging.WARNING)
    #     logging.getLogger('strands.telemetry.metrics').setLevel(logging.WARNING)
    # else:
    #     # In debug mode, show everything
    #     logging.getLogger('botocore').setLevel(logging.DEBUG)
    #     logging.getLogger('strands').setLevel(logging.DEBUG)
    
    # Keep important loggers at INFO
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('fastapi').setLevel(logging.INFO)
    logging.getLogger('agents.onboarding').setLevel(logging.INFO)
    
    # Set our application loggers to INFO or DEBUG
    logging.getLogger('__main__').setLevel(logging.DEBUG if debug_mode else logging.INFO)
    logging.getLogger('api_server').setLevel(logging.DEBUG if debug_mode else logging.INFO)


def get_logger(name: str) -> Logger:
    return logging.getLogger(name)
