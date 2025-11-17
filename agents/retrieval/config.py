"""
Configuration for the RAG Chat Agent.
"""

import os
from dotenv import load_dotenv
from agents.retrieval.backend import RETRIEVAL_BACKEND_PATH

# Load environment variables
load_dotenv()


class RAGChatConfig:
    """Configuration settings for the RAG chat agent."""
    
    # AWS Bedrock Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    
    # Model Configuration - using Claude Sonnet 4 on Bedrock
    MODEL_ID = os.getenv(
        "BEDROCK_MODEL_ID",
        "us.anthropic.claude-sonnet-4-20250514-v1:0"
    )
    
    # Agent Configuration
    AGENT_NAME = "RAGChatAssistant"
    AGENT_DESCRIPTION = "Intelligent tutor that retrieves and explains educational content"
    
    # RAG System Configuration
    RAG_DB_PATH = os.getenv("RAG_DB_PATH", f"{RETRIEVAL_BACKEND_PATH}/vector_db")
    RAG_MODEL_NAME = os.getenv("RAG_MODEL_NAME", "all-MiniLM-L6-v2")
    # RAG_MODEL_NAME = os.getenv("RAG_MODEL_NAME", "BAAI/bge-m3")
    
    # Keyword Extractor Configuration
    KEYWORDS_FILE = os.getenv("KEYWORDS_FILE", f"{RETRIEVAL_BACKEND_PATH}/probability_keywords.csv")
    NER_MODEL_PATH = os.getenv("NER_MODEL_PATH", f"{RETRIEVAL_BACKEND_PATH}/math_ner_model")
    
    # Retrieval Configuration
    DEFAULT_K = int(os.getenv("RAG_DEFAULT_K", "3"))  # Number of chunks to retrieve
    
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
