"""
RAG Chat Agent - Main agent implementation.
This agent provides intelligent tutoring using retrieval-augmented generation.
"""

from strands import Agent
from strands.models import BedrockModel
from typing import Optional
import logging

from agents.retrieval.config import RAGChatConfig
from agents.retrieval.prompts import AGENT_INSTRUCTIONS, WELCOME_MESSAGE
from agents.retrieval.tools import (
    rag_chat_tools,
    get_tools_instance
)

# Set up logger
logger = logging.getLogger(__name__)


class RAGChatAgent:
    """
    RAG Chat Agent for intelligent educational tutoring.
    
    This agent uses retrieval-augmented generation to provide high-quality,
    accurate educational content about probability and statistics. It combines:
    - Semantic search over a knowledge base
    - Keyword extraction for topic identification
    - Metadata filtering for precise content retrieval
    - LLM-based explanations and teaching
    """
    
    def __init__(self, config: Optional[RAGChatConfig] = None):
        """
        Initialize the RAG Chat Agent.
        
        Args:
            config: Optional configuration object. Uses default if not provided.
        """
        self.config = config or RAGChatConfig()
        
        # Initialize the tools backend (RAG system, keyword extractor)
        self._initialize_tools()
        
        # Create the Strands agent
        self.agent = self._create_agent()
        
        logger.info("RAG Chat Agent initialized successfully")
    
    def _initialize_tools(self):
        """Initialize the RAG system and keyword extractor."""
        logger.info("Initializing RAG tools...")
        
        # This will create the singleton tools instance
        get_tools_instance(
            rag_db_path=self.config.RAG_DB_PATH,
            keywords_file=self.config.KEYWORDS_FILE,
            ner_model_path=self.config.NER_MODEL_PATH
        )
        
        logger.info("RAG tools initialized")
    
    def _create_agent(self) -> Agent:
        """Create and configure the Strands agent."""
        
        # Create a configured Bedrock model
        model = BedrockModel(
            model_id=self.config.MODEL_ID,
            streaming=False,
        )
        
        try:
            agent = Agent(
                name=self.config.AGENT_NAME,
                model=model,
                system_prompt=AGENT_INSTRUCTIONS,
                tools=rag_chat_tools,
                description=self.config.AGENT_DESCRIPTION,
            )
            logger.info(f"✅ Agent created successfully with {len(rag_chat_tools)} tools")
        except Exception as e:
            logger.error(f"❌ Failed to create Agent/BedrockModel: {e}")
            raise
        
        return agent
    
    def chat(self, message: str, user_profile=None, **kwargs) -> str:
        """
        Chat interface for educational tutoring.
        
        Args:
            message: User's message/question
            user_profile: Optional UserProfile object for personalization
            **kwargs: Additional arguments passed to agent
        
        Returns:
            Agent's response
        """
        # Enhance message with user profile context if available
        if user_profile:
            profile_context = self._build_profile_context(user_profile)
            enhanced_message = f"{profile_context}\n\nUser Query: {message}"
        else:
            enhanced_message = message
        
        response = self.agent(enhanced_message, **kwargs)
        return str(response)
    
    def _build_profile_context(self, user_profile) -> str:
        """
        Build context string from user profile for personalized retrieval.
        
        Args:
            user_profile: UserProfile object
            
        Returns:
            Formatted context string
        """
        context_parts = [
            "[User Profile Context for Personalized Content Retrieval]"
        ]
        
        # Add competence level
        if hasattr(user_profile, 'competence_level') and user_profile.competence_level:
            level_map = {
                'beginner': 'basic',
                'intermediate': 'intermediate',
                'advanced': 'advanced',
                'basic': 'basic',
                'medium': 'intermediate',
                'high': 'advanced'
            }
            difficulty = level_map.get(user_profile.competence_level.lower(), 'intermediate')
            context_parts.append(f"Student Level: {user_profile.competence_level.title()} (retrieve '{difficulty}' difficulty content)")
        
        # # Add ability score
        # if hasattr(user_profile, 'ability_score') and user_profile.ability_score is not None:
        #     context_parts.append(f"Ability Score: {user_profile.ability_score:.2f}")
        
        # Add strengths
        if hasattr(user_profile, 'strengths') and user_profile.strengths:
            strengths_str = ", ".join(user_profile.strengths[:3])  # Limit to top 3
            context_parts.append(f"Strong Topics: {strengths_str}")
        
        # Add weaknesses
        if hasattr(user_profile, 'weaknesses') and user_profile.weaknesses:
            weaknesses_str = ", ".join(user_profile.weaknesses[:3])  # Limit to top 3
            context_parts.append(f"Areas for Improvement: {weaknesses_str}")
            context_parts.append("(Provide extra support and simpler explanations for these topics)")
        
        context_parts.append("\nIMPORTANT: Use the search_knowledge_base tool with the appropriate 'difficulty_level' parameter based on the student's level.")
        context_parts.append("For weak topics, consider retrieving prerequisite concepts first.")
        
        return "\n".join(context_parts)
    
    async def chat_async(self, message: str, user_profile=None, **kwargs) -> str:
        """
        Async chat interface for educational tutoring.
        
        Args:
            message: User's message/question
            user_profile: Optional UserProfile object for personalization
            **kwargs: Additional arguments passed to agent
        
        Returns:
            Agent's response
        """
        # Enhance message with user profile context if available
        if user_profile:
            profile_context = self._build_profile_context(user_profile)
            enhanced_message = f"{profile_context}\n\nUser Query: {message}"
        else:
            enhanced_message = message
        
        response = await self.agent.invoke_async(enhanced_message, **kwargs)
        return str(response)
    
    def welcome(self) -> str:
        """
        Get a welcome message for new users.
        
        Returns:
            Welcome message
        """
        return WELCOME_MESSAGE
    
    def __call__(self, message: str, **kwargs) -> str:
        """
        Make the agent callable directly.
        
        Args:
            message: User's message/question
            **kwargs: Additional arguments passed to agent
        
        Returns:
            Agent's response
        """
        return self.chat(message, **kwargs)


# Convenience function for quick agent creation
def create_rag_chat_agent(config: Optional[RAGChatConfig] = None) -> RAGChatAgent:
    """
    Create a RAG Chat Agent with optional custom configuration.
    
    Args:
        config: Optional configuration object
    
    Returns:
        Initialized RAGChatAgent instance
    
    Example:
        >>> agent = create_rag_chat_agent()
        >>> response = agent.chat("What is conditional probability?")
    """
    return RAGChatAgent(config=config)
