"""
Configuration for the Report Agent.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ReportConfig:
    """Configuration for Report Agent."""
    
    # Agent Configuration
    AGENT_NAME: str = "ReportAgent"
    AGENT_DESCRIPTION: str = "Generates comprehensive learning progress reports and analytics"
    
    # Model Configuration
    MODEL_ID: str = "us.anthropic.claude-sonnet-4-20250514-v1:0"
    
    # Report Settings
    DEFAULT_PERIOD_DAYS: int = 7  # Default report period in days
    MIN_DATA_POINTS: int = 2  # Minimum data points required for trends
    
    # Thresholds for classifications
    MASTERY_THRESHOLD: float = 0.80  # 80% accuracy to consider topic mastered
    WEAK_TOPIC_THRESHOLD: float = 0.60  # Below 60% is considered weak
    IMPROVEMENT_THRESHOLD: float = 0.05  # 5% improvement to consider "improving"
    
    # Time-series settings
    SNAPSHOT_TYPES: list = None  # ["daily", "weekly", "monthly"]
    
    def __post_init__(self):
        if self.SNAPSHOT_TYPES is None:
            self.SNAPSHOT_TYPES = ["daily", "weekly", "monthly"]


# Default configuration instance
default_config = ReportConfig()
