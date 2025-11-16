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
    
    def chat(self, message: str, **kwargs) -> str:
        """
        Chat interface for educational tutoring.
        
        Args:
            message: User's message/question
            **kwargs: Additional arguments passed to agent
        
        Returns:
            Agent's response
        """
        response = self.agent(message, **kwargs)
        return str(response)
    
    async def chat_async(self, message: str, **kwargs) -> str:
        """
        Async chat interface for educational tutoring.
        
        Args:
            message: User's message/question
            **kwargs: Additional arguments passed to agent
        
        Returns:
            Agent's response
        """
        response = await self.agent.invoke_async(message, **kwargs)
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
