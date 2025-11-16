"""
Orchestrator Agent - Multi-agent coordination using agents-as-tools pattern.

This orchestrator manages multiple specialized agents:
1. Onboarding Agent - User assessment and profiling
2. Content Generation Agent - PDF/Slides generation
3. RAG System - Knowledge retrieval (external)

The orchestrator intelligently routes requests to the appropriate agents based on user intent.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from strands import Agent, tool
from strands.models import BedrockModel

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.onboarding.agent import OnboardingAgent
from agents.content_generation.agent import ContentGenerator
from agents.orchestrator.adapter import create_content_generation_request
from shared.models import UserProfile
from agents.retrieval.backend.schema import Chunk

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """
    Main orchestrator that coordinates multiple specialized agents.
    
    Uses the agents-as-tools pattern where each specialized agent is wrapped
    as a tool that the orchestrator can invoke.
    """
    
    def __init__(self, rag_system=None):
        """
        Initialize the orchestrator with access to specialized agents.
        
        Args:
            rag_system: Optional RAG system instance for knowledge retrieval
        """
        self.rag_system = rag_system
        self.user_profiles: Dict[str, UserProfile] = {}
        
        # Initialize specialized agents
        self.onboarding_agent = OnboardingAgent()
        self.content_agent = ContentGenerator()
        
        # Create orchestrator agent with agents-as-tools
        self.agent = self._create_orchestrator()
        
        logger.info("✅ Orchestrator initialized with onboarding and content generation agents")
    
    def _create_orchestrator_tools(self):
        """Create tools that wrap specialized agents."""
        
        @tool
        def assess_new_user(user_id: str, total_questions: int = 10) -> Dict[str, Any]:
            """
            Assess a new user's knowledge level through adaptive testing.
            
            Use this tool when:
            - A new user needs to be onboarded
            - User asks to take an assessment or quiz
            - You need to determine user's competence level
            
            Args:
                user_id: Unique identifier for the user
                total_questions: Number of questions (default 10)
                
            Returns:
                User profile with competence level, strengths, weaknesses
            """
            try:
                logger.info(f"🔧 Orchestrator invoking onboarding agent for user: {user_id}")
                profile = self.onboarding_agent.assess_user(user_id, total_questions)
                
                # Store profile in memory
                self.user_profiles[user_id] = profile
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "competence_level": profile.competence_level,
                    "ability_score": profile.ability_score,
                    "final_score": profile.final_score,
                    "strengths": profile.strengths,
                    "weaknesses": profile.weaknesses,
                    "recommended_level": profile.recommended_starting_level
                }
            except Exception as e:
                logger.error(f"❌ Error in assess_new_user: {e}")
                return {"success": False, "error": str(e)}
        
        @tool
        def retrieve_knowledge(query: str, user_id: Optional[str] = None, 
                              max_chunks: int = 5) -> List[Dict[str, Any]]:
            """
            Retrieve relevant knowledge chunks from the RAG system.
            
            Use this tool when:
            - User asks a question that requires factual information
            - You need to gather content for PDF/slide generation
            - You need to provide explanations or examples
            
            Args:
                query: The search query or topic
                user_id: Optional user ID to personalize results based on their profile
                max_chunks: Maximum number of chunks to retrieve (default 5)
                
            Returns:
                List of relevant knowledge chunks with metadata
            """
            try:
                if not self.rag_system:
                    return {"success": False, "error": "RAG system not configured"}
                
                logger.info(f"🔧 Orchestrator querying RAG system: {query}")
                
                # Get user profile for personalization if available
                user_profile = None
                if user_id and user_id in self.user_profiles:
                    user_profile = self.user_profiles[user_id]
                
                # Query RAG system (this is a placeholder - replace with actual RAG call)
                chunks = self.rag_system.query(
                    query=query,
                    user_profile=user_profile,
                    max_results=max_chunks
                )
                
                # Convert Chunk objects to dictionaries
                results = []
                for chunk in chunks:
                    if isinstance(chunk, Chunk):
                        results.append({
                            "id": chunk.id,
                            "text": chunk.text,
                            "topics": chunk.metadata.topics,
                            "chunk_type": chunk.metadata.chunk_type,
                            "difficulty_level": chunk.metadata.difficulty_level,
                            "prerequisites": chunk.metadata.prerequisites,
                            "source_url": chunk.metadata.source_url
                        })
                    else:
                        results.append(chunk)
                
                return {
                    "success": True,
                    "query": query,
                    "chunks": results,
                    "count": len(results)
                }
                
            except Exception as e:
                logger.error(f"❌ Error in retrieve_knowledge: {e}")
                return {"success": False, "error": str(e)}
        
        @tool
        def generate_content(request_type: str, topic: str, user_id: Optional[str] = None,
                           num_slides: Optional[int] = None, 
                           include_exercises: bool = False) -> Dict[str, Any]:
            """
            Generate PDF documents or presentation slides using retrieved knowledge.
            
            Use this tool when:
            - User asks to create slides, presentation, or PPT
            - User asks to generate a PDF, document, or report
            - User wants structured learning materials
            
            Args:
                request_type: Type of content ('slides' or 'pdf')
                topic: The topic or title for the content
                user_id: Optional user ID to personalize content
                num_slides: Number of slides (for presentations, default 10)
                include_exercises: Whether to include practice problems
                
            Returns:
                Path to generated file and metadata
            """
            try:
                logger.info(f"🔧 Orchestrator generating {request_type} for topic: {topic}")
                
                # 1. Retrieve relevant knowledge from RAG
                rag_response = retrieve_knowledge(
                    query=topic,
                    user_id=user_id,
                    max_chunks=10
                )
                
                if not rag_response.get("success"):
                    return {"success": False, "error": "Failed to retrieve knowledge"}
                
                chunks = rag_response.get("chunks", [])
                
                # 2. Get user profile if available
                user_profile = None
                if user_id and user_id in self.user_profiles:
                    user_profile = self.user_profiles[user_id]
                
                # 3. Use adapter to create agent-ready request
                agent_request = create_content_generation_request(
                    topic=topic,
                    request_type=request_type,
                    rag_chunks=chunks,
                    user_profile=user_profile,
                    num_slides=num_slides,
                    include_exercises=include_exercises
                )
                
                # 4. Invoke content generation agent
                result = self.content_agent.chat(agent_request["prompt"])
                
                return {
                    "success": True,
                    "request_type": request_type,
                    "topic": topic,
                    "result": result,
                    "metadata": agent_request["metadata"]
                }
                
            except Exception as e:
                logger.error(f"❌ Error in generate_content: {e}")
                return {"success": False, "error": str(e)}
        
        @tool
        def get_user_profile(user_id: str) -> Dict[str, Any]:
            """
            Retrieve stored user profile information.
            
            Use this tool when:
            - You need to personalize responses for a user
            - You want to check a user's competence level
            - You need to understand user's strengths/weaknesses
            
            Args:
                user_id: The user's unique identifier
                
            Returns:
                User profile data or error if not found
            """
            if user_id in self.user_profiles:
                profile = self.user_profiles[user_id]
                return {
                    "success": True,
                    "user_id": user_id,
                    "competence_level": profile.competence_level,
                    "ability_score": profile.ability_score,
                    "strengths": profile.strengths,
                    "weaknesses": profile.weaknesses,
                    "recommended_level": profile.recommended_starting_level
                }
            else:
                return {
                    "success": False,
                    "error": f"No profile found for user {user_id}"
                }
        
        return [
            assess_new_user,
            retrieve_knowledge,
            generate_content,
            get_user_profile
        ]
    
    def _create_orchestrator(self) -> Agent:
        """Create the main orchestrator agent."""
        
        system_prompt = """You are an intelligent learning management orchestrator.

Your role is to coordinate multiple specialized agents to help users learn effectively:

1. **Onboarding Agent** - Assesses new users to determine their knowledge level
2. **RAG System** - Retrieves relevant educational content and explanations  
3. **Content Generator** - Creates PDF documents and presentation slides

**When to use each tool:**

- **assess_new_user**: When user is new, wants assessment, or you need their competence level
- **retrieve_knowledge**: When user asks questions or you need content for generation
- **generate_content**: When user wants slides, presentations, PDFs, or structured materials
- **get_user_profile**: When you need to personalize responses for a known user

**Best Practices:**

1. For new users, start with assessment to understand their level
2. Always retrieve knowledge before generating content
3. Personalize content based on user's competence level and learning pace
4. Be conversational and guide users through the learning process
5. If generating content, first gather knowledge, then create structured materials

**Content Generation Guidelines:**

- For slides: Keep each slide focused on one concept
- For PDFs: Organize into logical sections with clear headings
- Match difficulty to user's level (if known)
- Include examples and exercises when appropriate

Be helpful, educational, and always aim to provide the best learning experience."""

        model = BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=False,
        )
        
        tools = self._create_orchestrator_tools()
        
        agent = Agent(
            name="Learning Orchestrator",
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            description="Intelligent orchestrator for multi-agent learning system"
        )
        
        return agent
    
    def chat(self, user_message: str, user_id: Optional[str] = None) -> str:
        """
        Process user message through orchestrator.
        
        Args:
            user_message: The user's message/request
            user_id: Optional user ID for context
            
        Returns:
            Orchestrator's response
        """
        # Add user context to message if available
        if user_id and user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            context = f"\n[User Context: {user_id}, Level: {profile.competence_level}]\n"
            message = context + user_message
        else:
            message = user_message
        
        logger.info(f"💬 Orchestrator processing: {user_message[:100]}...")
        response = self.agent.chat(message)
        
        return response
    
    def set_rag_system(self, rag_system):
        """Set or update the RAG system instance."""
        self.rag_system = rag_system
        logger.info("✅ RAG system configured")


# Convenience function for FastAPI integration
def create_orchestrator(rag_system=None) -> OrchestratorAgent:
    """
    Factory function to create orchestrator instance.
    
    Args:
        rag_system: Optional RAG system instance
        
    Returns:
        Configured OrchestratorAgent
    """
    return OrchestratorAgent(rag_system=rag_system)


if __name__ == "__main__":
    # Simple test
    logging.basicConfig(level=logging.INFO)
    
    print("Creating orchestrator...")
    orchestrator = create_orchestrator()
    
    print("\nTest 1: Simple query")
    response = orchestrator.chat("Hello! I'm new here.")
    print(f"Response: {response}")
    
    print("\nOrchestrator test complete!")
