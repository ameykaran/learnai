"""
RAG Chat Agent Tools - Strands tools for intelligent content retrieval.
These tools wrap the RAG system and keyword extraction functionality.
"""

import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Literal

from strands import tool


from agents.retrieval.backend.rag_system import RAGSystem
from agents.retrieval.backend.keyword_extractor import KeywordExtractor
from agents.retrieval.backend import RETRIEVAL_BACKEND_PATH
import dspy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RAGChatTools:
    """
    Collection of tools for the RAG chat agent.
    These tools provide intelligent content retrieval from the knowledge base.
    """
    
    def __init__(
        self,
        rag_db_path: str = f"{RETRIEVAL_BACKEND_PATH}/vector_db",
        keywords_file: str = f"{RETRIEVAL_BACKEND_PATH}/probability_keywords.csv",
        ner_model_path: str = f"{RETRIEVAL_BACKEND_PATH}/math_ner_model"
    ):
        """Initialize tools with RAG system and keyword extractor."""
        logger.info("=" * 60)
        logger.info("Initializing RAG Chat Tools...")
        logger.info(f"RAG DB Path: {rag_db_path}")
        logger.info(f"Keywords File: {keywords_file}")
        logger.info(f"NER Model Path: {ner_model_path}")
        
        # Check if paths exist
        db_path = Path(rag_db_path)
        logger.info(f"Checking if RAG DB path exists: {db_path.absolute()}")
        logger.info(f"RAG DB path exists: {db_path.exists()}")
        if db_path.exists():
            logger.info(f"Contents of RAG DB directory: {list(db_path.iterdir())}")
        
        # Initialize RAG system
        logger.info("Initializing RAG system...")
        try:
            self.rag_system = RAGSystem(db_path=rag_db_path)
            chunk_count = self.rag_system.collection.count()
            logger.info(f"✓ RAG system initialized successfully")
            logger.info(f"✓ Collection name: {self.rag_system.collection.name}")
            logger.info(f"✓ Total chunks in collection: {chunk_count}")
            
            if chunk_count == 0:
                logger.warning("⚠️  WARNING: Knowledge base is EMPTY (0 chunks)")
                logger.warning("⚠️  You may need to initialize the database with content")
                logger.warning(f"⚠️  Expected database at: {db_path.absolute()}")
            else:
                logger.info(f"✓ Knowledge base loaded with {chunk_count} chunks")
                
        except Exception as e:
            logger.error(f"✗ Failed to initialize RAG system: {e}", exc_info=True)
            raise
        
        # Initialize keyword extractor
        logger.info("Initializing keyword extractor...")
        try:
            self.keyword_extractor = KeywordExtractor(
                keywords_file=keywords_file,
                model_path=ner_model_path
            )
            logger.info(f"✓ Keyword extractor initialized")
        except Exception as e:
            logger.error(f"✗ Failed to initialize keyword extractor: {e}", exc_info=True)
            raise
        
        # Initialize DSPy for metadata extraction
        logger.info("Initializing DSPy metadata extractor...")
        try:
            self.lm = dspy.LM(
                # model="gemini/gemini-2.0-flash-exp",
                model="bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0",
                max_tokens=1000,
                num_retries=3,
                temperature=0.2
            )
            dspy.configure(lm=self.lm)
            logger.info(f"✓ Metadata extractor initialized")
        except Exception as e:
            logger.error(f"✗ Failed to initialize metadata extractor: {e}", exc_info=True)
            raise
        
        logger.info("=" * 60)
        logger.info("RAG Chat Tools initialization complete!")
        logger.info("=" * 60)
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract mathematical keywords from a query."""
        logger.debug(f"Extracting keywords from query: {query}")
        keywords = self.keyword_extractor.extract_keywords(query)
        logger.debug(f"Extracted keywords: {keywords}")
        return keywords
    
    def determine_chunk_type(self, query: str) -> str:
        """Use LLM to determine the most appropriate chunk type for the query."""
        logger.debug(f"Determining chunk type for query: {query}")
        
        class MetadataExtractor(dspy.Signature):
            query: str = dspy.InputField(desc="User query about a concept.")
            chunk_type: Literal[
                "definition", "example", "explanation", "proof", 
                "visualization", "practice_problem", "worked_solution", 
                "analogy", "misconception"
            ] = dspy.OutputField(desc="Type of chunk to extract.")
        
        extractor = dspy.Predict(MetadataExtractor)
        try:
            result = extractor(query=query)
            logger.debug(f"Determined chunk type: {result.chunk_type}")
            return result.chunk_type
        except Exception as e:
            logger.error(f"Error determining chunk type: {e}", exc_info=True)
            logger.info("Falling back to default chunk type: explanation")
            return "explanation"  # Default fallback


# Create a singleton instance
_tools_instance = None


def get_tools_instance(
    rag_db_path: str = f"{RETRIEVAL_BACKEND_PATH}/vector_db",
    keywords_file: str = f"{RETRIEVAL_BACKEND_PATH}/probability_keywords.csv",
    ner_model_path: str = f"{RETRIEVAL_BACKEND_PATH}/math_ner_model"
) -> RAGChatTools:
    """Get or create the tools instance (singleton pattern)."""
    global _tools_instance
    if _tools_instance is None:
        _tools_instance = RAGChatTools(rag_db_path, keywords_file, ner_model_path)
    return _tools_instance


@tool
def search_knowledge_base(
    query: str,
    chunk_type: Optional[Literal[
        "definition", "example", "explanation", "proof", 
        "visualization", "practice_problem", "worked_solution", 
        "analogy", "misconception"
    ]] = None,
    topics: Optional[List[str]] = None,
    difficulty_level: Optional[Literal["basic", "intermediate", "advanced"]] = None,
    k: int = 3
) -> str:
    """
    Search the educational knowledge base for relevant content.
    
    This tool retrieves content from a comprehensive database of educational materials
    about probability and statistics. It uses semantic search combined with metadata
    filtering to find the most relevant content.
    
    Args:
        query: The student's question or topic to search for (e.g., "conditional probability", 
               "What is Bayes theorem?", "How do I calculate expected value?")
        chunk_type: The type of content to retrieve. If not specified, automatically determined.
                   - "definition": Formal definition of a concept
                   - "example": Concrete example demonstrating the concept
                   - "explanation": Detailed explanation of the topic
                   - "proof": Mathematical proof of a theorem
                   - "visualization": Visual representation or diagram
                   - "practice_problem": Problem for the student to solve
                   - "worked_solution": Step-by-step solution to a problem
                   - "analogy": Relatable analogy to explain the concept
                   - "misconception": Common mistakes and how to avoid them
        topics: Optional list of specific topics to filter by (e.g., ["probability", "statistics"])
                If not provided, automatically extracted from the query
        difficulty_level: Optional difficulty filter - "basic", "intermediate", or "advanced"
        k: Number of content pieces to retrieve (default: 3, range: 1-10)
    
    Returns:
        A formatted string containing the retrieved educational content with metadata
    
    Examples:
        # Get a definition
        search_knowledge_base("What is conditional probability?", chunk_type="definition")
        
        # Get examples with specific topics
        search_knowledge_base("probability distributions", chunk_type="example", topics=["probability"])
        
        # Get basic explanations
        search_knowledge_base("random variables", chunk_type="explanation", difficulty_level="basic")
        
        # Get practice problems
        search_knowledge_base("Bayes theorem", chunk_type="practice_problem")
        
        # Let the system determine the best content type
        search_knowledge_base("I don't understand independence")
    """
    logger.info("=" * 60)
    logger.info("SEARCH_KNOWLEDGE_BASE Tool Called")
    logger.info(f"Query: {query}")
    logger.info(f"Requested chunk_type: {chunk_type}")
    logger.info(f"Requested topics: {topics}")
    logger.info(f"Requested difficulty_level: {difficulty_level}")
    logger.info(f"Requested k: {k}")
    
    tools = get_tools_instance()
    
    # Log RAG system status
    collection_count = tools.rag_system.collection.count()
    logger.info(f"Current RAG collection count: {collection_count}")
    
    if collection_count == 0:
        logger.error("⚠️  CRITICAL: Knowledge base is EMPTY!")
        logger.error("⚠️  No chunks available for retrieval")
        logger.error("⚠️  Database needs to be initialized with content")
        return "ERROR: The knowledge base is empty. Please initialize the database with educational content before using the search function."
    
    # Extract keywords if topics not provided
    if topics is None:
        logger.info("Topics not provided, extracting keywords from query...")
        keywords = tools.extract_keywords(query)
        logger.info(f"Extracted keywords: {keywords}")
        topics = [kw.lower() for kw in keywords] if keywords else None
        logger.info(f"Converted to topics: {topics}")
    
    # Determine chunk type if not provided
    if chunk_type is None:
        logger.info("Chunk type not provided, determining from query...")
        chunk_type = tools.determine_chunk_type(query)
        logger.info(f"Determined chunk_type: {chunk_type}")
    
    # Build filters
    filters = {}
    if topics:
        filters["topics"] = topics
    if chunk_type:
        filters["chunk_type"] = chunk_type
    if difficulty_level:
        filters["difficulty_level"] = difficulty_level
    
    logger.info(f"Final filters being applied: {filters}")
    
    # Perform retrieval
    logger.info(f"Calling RAG system query with k={k}...")
    try:
        chunks = tools.rag_system.query(query, k=k, filters=filters, verbose=True)
        logger.info(f"RAG system returned {len(chunks)} chunks")
    except Exception as e:
        logger.error(f"Error during RAG system query: {e}", exc_info=True)
        return f"ERROR: Failed to query knowledge base: {str(e)}"
    
    # Format results
    if not chunks:
        logger.warning(f"No chunks found for query: {query}")
        logger.warning(f"Filters used: {filters}")
        return f"No content found for '{query}' with the specified filters. Try broadening your search or using different keywords."
    
    logger.info(f"Successfully retrieved {len(chunks)} chunks, formatting results...")
    result = f"Found {len(chunks)} relevant content piece(s):\n\n"
    
    for i, chunk in enumerate(chunks, 1):
        result += f"=== Content {i} ===\n"
        result += f"Type: {chunk.metadata.chunk_type}\n"
        result += f"Topics: {', '.join(chunk.metadata.topics)}\n"
        result += f"Difficulty: {chunk.metadata.difficulty_level}\n"
        if chunk.metadata.prerequisites:
            result += f"Prerequisites: {', '.join(chunk.metadata.prerequisites)}\n"
        result += f"\n{chunk.text}\n"
        result += f"\nSource: {chunk.metadata.source_url}\n"
        result += "-" * 50 + "\n\n"
    
    return result


@tool
def get_related_topics(topic: str, k: int = 5) -> str:
    """
    Find topics related to a given concept.
    
    Use this when a student wants to explore related concepts or when you want
    to provide broader context for a topic.
    
    Args:
        topic: The main topic to find related concepts for
        k: Number of related topics to retrieve (default: 5)
    
    Returns:
        A formatted string listing related topics with brief descriptions
    
    Example:
        get_related_topics("conditional probability")
    """
    tools = get_tools_instance()
    
    # Search for content mentioning this topic
    chunks = tools.rag_system.query(
        f"topics related to {topic}",
        k=k,
        filters=None,
        verbose=False
    )
    
    if not chunks:
        return f"Could not find related topics for '{topic}'"
    
    # Extract unique topics from retrieved chunks
    related_topics = set()
    for chunk in chunks:
        related_topics.update(chunk.metadata.topics)
    
    # Remove the original topic
    related_topics.discard(topic.lower())
    
    result = f"Topics related to '{topic}':\n\n"
    for related_topic in sorted(related_topics):
        result += f"- {related_topic}\n"
    
    return result


@tool
def get_prerequisites(topic: str) -> str:
    """
    Identify prerequisite concepts for a given topic.
    
    Use this when a student is struggling with a concept and might need to
    learn foundational topics first.
    
    Args:
        topic: The topic to find prerequisites for
    
    Returns:
        A formatted string listing prerequisite concepts
    
    Example:
        get_prerequisites("Bayes theorem")
    """
    tools = get_tools_instance()
    
    # Search for content about this topic
    chunks = tools.rag_system.query(
        topic,
        k=3,
        filters=None,
        verbose=False
    )
    
    if not chunks:
        return f"Could not find prerequisite information for '{topic}'"
    
    # Extract unique prerequisites
    prerequisites = set()
    for chunk in chunks:
        if chunk.metadata.prerequisites:
            prerequisites.update(chunk.metadata.prerequisites)
    
    if not prerequisites:
        return f"No specific prerequisites found for '{topic}'. This may be a foundational topic."
    
    result = f"Prerequisites for '{topic}':\n\n"
    for prereq in sorted(prerequisites):
        result += f"- {prereq}\n"
    
    result += "\nWould you like me to explain any of these prerequisite concepts first?"
    
    return result


@tool
def get_knowledge_base_stats() -> str:
    """
    Get statistics about the knowledge base.
    
    Use this to understand what content is available and help students
    understand the scope of topics you can help with.
    
    Returns:
        A formatted string with knowledge base statistics
    """
    logger.info("=" * 60)
    logger.info("GET_KNOWLEDGE_BASE_STATS Tool Called")
    
    tools = get_tools_instance()
    
    try:
        stats = tools.rag_system.get_stats()
        logger.info(f"Retrieved stats: {stats}")
        
        total_chunks = stats.get('total_chunks', 0)
        logger.info(f"Total chunks in database: {total_chunks}")
        
        if total_chunks == 0:
            logger.error("⚠️  CRITICAL: Knowledge base is EMPTY!")
            logger.error("⚠️  Stats show 0 chunks available")
            result = "⚠️  WARNING: The knowledge base is currently EMPTY.\n\n"
            result += "No educational content has been loaded into the database.\n"
            result += "Please initialize the database with content before using the retrieval system.\n\n"
            result += "To initialize, you typically need to:\n"
            result += "1. Prepare your content in the correct JSON format\n"
            result += "2. Run the initialization script (e.g., initialize_rag_system())\n"
            result += "3. Verify the content was loaded successfully\n"
            return result
        
        result = "Knowledge Base Statistics:\n\n"
        result += f"Total content pieces: {stats['total_chunks']}\n"
        
        if 'chunk_types' in stats:
            result += f"\nContent types available:\n"
            for chunk_type, count in stats['chunk_types'].items():
                result += f"- {chunk_type}: {count}\n"
        
        if 'difficulty_levels' in stats:
            result += f"\nDifficulty levels:\n"
            for level, count in stats['difficulty_levels'].items():
                result += f"- {level}: {count}\n"
        
        logger.info("Successfully generated stats report")
        logger.info("=" * 60)
        return result
        
    except Exception as e:
        logger.error(f"Error getting knowledge base stats: {e}", exc_info=True)
        return f"ERROR: Failed to retrieve knowledge base statistics: {str(e)}"


# Export the tools list for the agent
rag_chat_tools = [
    search_knowledge_base,
    get_related_topics,
    get_prerequisites,
    get_knowledge_base_stats
]
