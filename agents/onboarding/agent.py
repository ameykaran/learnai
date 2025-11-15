"""
Onboarding Agent - Main agent implementation.
This agent administers adaptive probability assessments for new students.
"""

from strands import Agent
from strands.models import BedrockModel
from typing import Optional
import sys
import logging
from pathlib import Path
# from strands.models.gemini import GeminiModel

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
    finalize_assessment,
    onboarding_tools  # Import the tools instance
)
from shared.models import UserProfile

# Set up logger
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
        self.tools_instance = onboarding_tools  # Expose tools instance for profile access
    
    def _create_agent(self) -> Agent:
        """Create and configure the Strands agent."""
        # model = GeminiModel(
        #     client_args={
        #         "api_key": os.getenv("GEMINI_API_KEY")
        #     },
        #     model_id=self.config.MODEL_ID,
        # )

        # Create a configured Bedrock model
        model = BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=False,
        )

        try:
            agent = Agent(
                    name=self.config.AGENT_NAME,
                    model=model,
                    system_prompt=AGENT_INSTRUCTIONS,
                    tools=[
                        start_assessment,
                        get_next_question,
                        submit_answer,
                        get_progress,
                        finalize_assessment,
                    ],
                    description=self.config.AGENT_DESCRIPTION,
                )
            logger.info("✅ Agent created successfully with 5 tools")
        except Exception as e:
            logger.error(f"❌ Failed to create Agent/BedrockModel: {e}")
            raise

        return agent
    
    def assess_user(self, user_id: str, total_questions: Optional[int] = None) -> UserProfile:
        """
        Run a complete assessment for a user.
        
        This is the main entry point for the orchestrator to initiate onboarding.
        The agent will guide the user through the assessment and return their profile.
        
        Args:
            user_id: Unique identifier for the user
            total_questions: Optional override for number of questions
        
        Returns:
            UserProfile object to be stored in orchestrator memory
        """
        self.current_user_id = user_id
        
        # Initial message to start assessment
        initial_message = f"Please start an assessment for user {user_id}"
        if total_questions:
            initial_message += f" with {total_questions} questions"
        
        # Run the agent
        response = self.chat(initial_message)
        
        # Return the generated profile (this would be extracted from agent conversation)
        # In practice, the orchestrator would monitor tool calls and extract the profile
        return response
    
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
        return str(response)
    
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
        return str(response)
    
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
