"""
Configuration for the Onboarding Agent.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OnboardingConfig:
    """Configuration settings for the onboarding agent."""
    
    # AWS Bedrock Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    
    # Model Configuration - using Claude Sonnet 4 on Bedrock
    MODEL_ID = os.getenv(
        "BEDROCK_MODEL_ID",
        # "anthropic.claude-sonnet-4-20250514-v1:0"
        # "anthropic.claude-sonnet-4-20250514-v1:0"
        # f"{AWS_REGION}.anthropic.claude-sonnet-4-20250514-v1:0"
    )
    
    # Agent Configuration
    AGENT_NAME = "OnboardingAssessor"
    AGENT_DESCRIPTION = "Adaptive probability assessment agent for student onboarding"
    
    # Quiz Configuration
    DEFAULT_TOTAL_QUESTIONS = int(os.getenv("ONBOARDING_TOTAL_QUESTIONS", "25"))
    
    # Verbose logging
    VERBOSE = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    
    @classmethod
    def get_bedrock_config(cls) -> dict:
        """Get Bedrock model provider configuration."""
        return {
            "provider": "bedrock",
            "model_id": cls.MODEL_ID,
            "region": cls.AWS_REGION,
        }
