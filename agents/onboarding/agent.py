"""
Onboarding Agent - Main agent implementation.
This agent administers adaptive probability assessments for new students.
"""

from strands import Agent
from strands.models import BedrockModel
from typing import Optional
import sys
from pathlib import Path

# Add shared module to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from .config import OnboardingConfig
from .prompts import AGENT_INSTRUCTIONS
from .tools import (
    start_assessment,
    get_next_question,
    submit_answer,
    get_progress,
    finalize_assessment
)
from shared.models import UserProfile
import logging

logger = logging.getLogger(__name__)

class OnboardingAgent:
    """
    Onboarding Agent for adaptive probability assessment.
    
    This agent administers a prerequisite quiz to determine student competence level.
    It uses the adaptive algorithm from the existing backend and generates a UserProfile
    that can be stored in the orchestrator's memory for use by other agents.
    """
    
    def __init__(self, config: Optional[OnboardingConfig] = None):
        """
        Initialize the Onboarding Agent.
        
        Args:
            config: Optional configuration object. Uses default if not provided.
        """
        self.config = config or OnboardingConfig()
        self.agent = self._create_agent()
        self.current_user_id = None
        self.current_session_id = None
    
    def _create_agent(self) -> Agent:
        """Create and configure the Strands agent."""
        
        # Create a Bedrock model that supports multimodal inputs
        bedrock_model = BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"
        )

        # Create agent with tools and instructions
        agent = Agent(
            name=self.config.AGENT_NAME,
            model=bedrock_model,
            system_prompt=AGENT_INSTRUCTIONS,
            tools=[
                start_assessment,
                get_next_question,
                submit_answer,
                get_progress,
                finalize_assessment
            ],
            description=self.config.AGENT_DESCRIPTION
        )
        
        return agent

    def chat(self, message: str, **kwargs) -> str:
        """
        Chat interface for interactive assessment.
        
        Args:
            message: User's message
            **kwargs: Additional arguments passed to agent
        
        Returns:
            Agent's response
        """
        response = self.agent(message, **kwargs)
        return response
    
    async def chat_async(self, message: str, **kwargs) -> str:
        """
        Async chat interface for interactive assessment.
        
        Args:
            message: User's message
            **kwargs: Additional arguments passed to agent
        
        Returns:
            Agent's response
        """
        response = await self.agent.invoke_async(message, **kwargs)
        return response
    
    def __call__(self, message: str, **kwargs) -> str:
        """
        Make the agent callable directly.
        
        Args:
            message: User's message
            **kwargs: Additional arguments
        
        Returns:
            Agent's response
        """
        return self.chat(message, **kwargs)


def create_onboarding_agent(
    user_id: Optional[str] = None,
    config: Optional[OnboardingConfig] = None
) -> OnboardingAgent:
    """
    Factory function to create an onboarding agent.
    
    Args:
        user_id: Optional user ID to set
        config: Optional configuration
    
    Returns:
        Configured OnboardingAgent instance
    """
    agent = OnboardingAgent(config=config)
    if user_id:
        agent.current_user_id = user_id
    return agent
