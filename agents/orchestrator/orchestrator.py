"""
Enhanced Workflow-Based Orchestrator
Consolidates classifier-based routing with structured agent coordination.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

from agents.orchestrator.classifier import Classifier
from agents.retrieval.agent import RAGChatAgent
from agents.content_generation.agent import ContentGenerator
from agents.specialist import get_specialist_agent
from shared.models import UserProfile

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Production-ready orchestrator using classifier-based workflow routing.
    
    Features:
    - Rule-based + LLM classification
    - Predefined workflows per query type
    - Structured logging with traces
    - User profile management
    - Sequential agent execution with context passing
    """
    
    def __init__(self):
        """
        Initialize orchestrator with specialized agents.
        
        Args:
            rag_system: Optional RAG system for retrieval agent
        """
        self.classifier = Classifier(llm_enabled=True)
        self.user_profiles: Dict[str, UserProfile] = {}
        
        # Initialize agents
        self.retriever = RAGChatAgent()
        self.content_agent = ContentGenerator()
        self.specialist_agent = None  # Lazy load specialist (heavy model)
        
        # Agent registry for dynamic invocation
        self.agents = {
            "retriever": self.retriever,
            "content_generation": self.content_agent,
            "specialist": lambda: self._get_specialist_agent(),
            # Add other agents here as they're implemented
            # "quiz": QuizAgent(),
            # "report": ReportAgent(),
        }
        
        logger.info("✅ WorkflowOrchestrator initialized with %d agents", len(self.agents))
    
    def _get_specialist_agent(self):
        """Lazy load the specialist agent (only when needed)."""
        if self.specialist_agent is None:
            logger.info("Loading specialist math agent (first use)...")
            self.specialist_agent = get_specialist_agent()
        return self.specialist_agent
    
    def process_query(
        self,
        query: str,
        user_id: Optional[str] = None,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Main entry point for processing user queries.
        
        Args:
            query: User's query string
            user_id: Optional user identifier for personalization
            context: Optional additional context
            
        Returns:
            Dict containing:
                - query: Original query
                - query_type: Classified query type
                - scores: Classification scores
                - steps: List of agent execution steps
                - final_response: Synthesized final response
                - metadata: Additional metadata (timing, user info, etc.)
        """
        start_ts = int(time.time() * 1000)
        
        logger.info(
            "incoming_query",
            extra={"extra_json": {"query": query, "user_id": user_id}}
        )
        
        # Step 1. Classify query
        qtype, scores = self.classifier.classify(query)
        workflow = self.classifier.query_types.get(qtype)
        
        logger.info(
            "classification",
            extra={
                "extra_json": {
                    "query": query,
                    "query_type": qtype,
                    "scores": scores,
                    "workflow": workflow.get("workflow", "unknown")
                }
            }
        )
        
        # Step 2. Get user profile if available
        user_profile = self.user_profiles.get(user_id) if user_id else None
        
        # Step 3. Execute workflow
        steps = []
        retrieved_context = ""
        
        # Step 3.1: Retrieval (if needed)
        if "retriever" in workflow.get("agents", []):
            retrieved_context = self._execute_retriever(
                query=query,
                context=context,
                user_profile=user_profile,
                steps=steps
            )
        
        # Step 3.2: Specialized agents
        for agent_name in workflow.get("agents", []):
            if agent_name == "retriever":
                continue  # Already executed
                
            self._execute_agent(
                agent_name=agent_name,
                query=query,
                retrieved_context=retrieved_context,
                user_id=user_id,
                user_profile=user_profile,
                steps=steps
            )
        
        # Step 4. Synthesize final response
        final_response = self._synthesize_response(steps, qtype)
        
        # Step 5. Create structured trace
        duration_ms = int(time.time() * 1000) - start_ts
        trace = self._create_trace(
            start_ts=start_ts,
            duration_ms=duration_ms,
            user_id=user_id,
            query=query,
            qtype=qtype,
            scores=scores,
            steps=steps,
            final_response=final_response
        )
        
        logger.info("orchestrator_trace", extra={"extra_json": trace})
        
        return {
            "query": query,
            "query_type": qtype,
            "scores": scores,
            "steps": steps,
            "final_response": final_response,
            "metadata": {
                "duration_ms": duration_ms,
                "user_id": user_id,
                "workflow": workflow.get("workflow"),
                "agents_used": [s["agent"] for s in steps]
            }
        }
    
    def _execute_retriever(
        self,
        query: str,
        context: str,
        user_profile: Optional[UserProfile],
        steps: List[Dict[str, Any]]
    ) -> str:
        """Execute retriever agent and track results."""
        if not self.retriever:
            logger.warning("Retriever not configured, skipping retrieval")
            return ""
        
        t0 = time.time()
        
        try:
            # Build retrieval query with context
            retrieval_query = f"{context}\n{query}" if context else query
            
            # Call retriever with user profile for personalization
            retrieved = self.retriever.chat(
                message=retrieval_query,
                user_profile=user_profile
            )
            
            duration_ms = int((time.time() - t0) * 1000)
            
            steps.append({
                "agent": "retriever",
                "output": retrieved,
                "duration_ms": duration_ms,
                "success": True
            })
            
            logger.info(
                "agent_step",
                extra={
                    "extra_json": {
                        "agent": "retriever",
                        "duration_ms": duration_ms,
                        "output_length": len(str(retrieved))
                    }
                }
            )
            
            return retrieved
            
        except Exception as e:
            logger.error(f"Retriever error: {e}", exc_info=True)
            steps.append({
                "agent": "retriever",
                "error": str(e),
                "success": False
            })
            return ""
    
    def _execute_agent(
        self,
        agent_name: str,
        query: str,
        retrieved_context: str,
        user_id: Optional[str],
        user_profile: Optional[UserProfile],
        steps: List[Dict[str, Any]]
    ):
        """Execute a specialized agent and track results."""
        t0 = time.time()
        
        try:
            # Route to appropriate agent
            if agent_name == "content_generation":
                output = self._call_content_generation(
                    query=query,
                    retrieved=retrieved_context,
                    user_profile=user_profile
                )
            elif agent_name == "quiz":
                output = self._call_quiz(
                    query=query,
                    retrieved=retrieved_context,
                    user_profile=user_profile
                )
            elif agent_name == "report":
                output = self._call_report(
                    user_id=user_id or "unknown",
                    user_profile=user_profile
                )
            elif agent_name == "specialist":
                output = self._call_specialist(
                    query=query,
                    retrieved=retrieved_context,
                    user_profile=user_profile
                )
            else:
                output = f"[Agent '{agent_name}' not yet implemented]"
                logger.warning(f"Unknown agent: {agent_name}")
            
            duration_ms = int((time.time() - t0) * 1000)
            
            steps.append({
                "agent": agent_name,
                "output": output,
                "duration_ms": duration_ms,
                "success": True
            })
            
            logger.info(
                "agent_step",
                extra={
                    "extra_json": {
                        "agent": agent_name,
                        "duration_ms": duration_ms,
                        "output_summary": str(output)[:500]
                    }
                }
            )
            
        except Exception as e:
            logger.error(f"Agent {agent_name} error: {e}", exc_info=True)
            steps.append({
                "agent": agent_name,
                "error": str(e),
                "success": False
            })
    
    # ========================================================================
    # AGENT CALL METHODS
    # ========================================================================
    
    def _call_content_generation(
        self,
        query: str,
        retrieved: str,
        user_profile: Optional[UserProfile]
    ) -> str:
        """Call content generation agent."""
        # Parse intent from query
        if "slide" in query.lower() or "presentation" in query.lower():
            request_type = "slides"
        else:
            request_type = "pdf"
        
        # Extract topic (simplified)
        topic = query.replace("create", "").replace("generate", "").strip()
        
        # Use content agent (placeholder - implement full logic)
        return f"[Content generation for '{topic}' as {request_type} - Implementation needed]"
    
    def _call_quiz(
        self,
        query: str,
        retrieved: str,
        user_profile: Optional[UserProfile]
    ) -> str:
        """Call quiz generation agent."""
        return "[Quiz generation - Implementation needed]"
    
    def _call_report(
        self,
        user_id: str,
        user_profile: Optional[UserProfile]
    ) -> str:
        """Call report generation agent."""
        if not user_profile:
            return "Cannot generate report: User profile not found. Please complete onboarding first."
        
        return "[Report generation - Implementation needed]"
    
    def _call_specialist(
        self,
        query: str,
        retrieved: str,
        user_profile: Optional[UserProfile]
    ) -> str:
        """Call specialist/math agent for problem solving.
        
        Args:
            query: The mathematical problem or question
            retrieved: Context from RAG system (examples, formulas, etc.)
            user_profile: Optional user profile for personalization
            
        Returns:
            Step-by-step solution from the specialist agent
        """
        try:
            # Get the specialist agent (lazy loaded)
            specialist = self._get_specialist_agent()
            
            # Call the agent with problem and context
            logger.info("Calling specialist agent with query: %s", query[:100])
            response = specialist(query, context=retrieved)
            
            logger.info("Specialist agent response received (%d chars)", len(str(response)))
            return str(response)
            
        except Exception as e:
            logger.error("Specialist agent error: %s", e, exc_info=True)
            return f"I encountered an error while solving this problem: {str(e)}"
    
    # ========================================================================
    # RESPONSE SYNTHESIS
    # ========================================================================
    
    def _synthesize_response(self, steps: List[Dict[str, Any]], qtype: str) -> str:
        """
        Synthesize final response from agent outputs.
        
        Args:
            steps: List of agent execution steps
            qtype: Query type for context
            
        Returns:
            Synthesized response string
        """
        if not steps:
            return "I couldn't process your query. Please try again."
        
        # Collect successful outputs
        successful_outputs = [
            step["output"] 
            for step in steps 
            if step.get("success", False) and "output" in step
        ]
        
        if not successful_outputs:
            return "An error occurred while processing your request."
        
        # Simple synthesis based on query type
        if qtype == "concept_explanation":
            return self._synthesize_explanation(successful_outputs)
        elif qtype == "assessment":
            return self._synthesize_assessment(successful_outputs)
        elif qtype == "performance_report":
            return successful_outputs[-1]  # Return report directly
        elif qtype == "content_creation":
            return self._synthesize_content_creation(successful_outputs)
        else:
            # Default: return last output
            return successful_outputs[-1]
    
    def _synthesize_explanation(self, outputs: List[str]) -> str:
        """Synthesize explanation from retriever + content agent."""
        if len(outputs) == 1:
            return outputs[0]
        
        # Combine retrieval context with generated explanation
        retrieval = outputs[0] if outputs else ""
        explanation = outputs[1] if len(outputs) > 1 else ""
        
        return f"{explanation}\n\n**Reference Information:**\n{retrieval}"
    
    def _synthesize_assessment(self, outputs: List[str]) -> str:
        """Synthesize assessment response."""
        return outputs[-1]  # Quiz agent output
    
    def _synthesize_content_creation(self, outputs: List[str]) -> str:
        """Synthesize content creation response."""
        return outputs[-1]  # Content agent output
    
    # ========================================================================
    # TRACING & LOGGING
    # ========================================================================
    
    def _create_trace(
        self,
        start_ts: int,
        duration_ms: int,
        user_id: Optional[str],
        query: str,
        qtype: str,
        scores: Dict,
        steps: List[Dict[str, Any]],
        final_response: str
    ) -> Dict[str, Any]:
        """Create structured trace for logging."""
        return {
            "timestamp_ms": start_ts,
            "duration_ms": duration_ms,
            "user_id": user_id,
            "query": query,
            "query_type": qtype,
            "classification_scores": scores,
            "steps": [
                {
                    "agent": s["agent"],
                    "duration_ms": s.get("duration_ms", 0),
                    "success": s.get("success", False),
                    "output_summary": str(s.get("output", ""))[:500],
                    "error": s.get("error")
                }
                for s in steps
            ],
            "final_response_length": len(final_response),
            "final_response_preview": final_response[:500]
        }
    
    # ========================================================================
    # PROFILE MANAGEMENT
    # ========================================================================
    
    def store_profile(self, user_id: str, profile: UserProfile):
        """Store user profile for future queries."""
        self.user_profiles[user_id] = profile
        logger.info(f"Profile stored for user: {user_id}")
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Retrieve user profile."""
        return self.user_profiles.get(user_id)
    
    # ========================================================================
    # CHAT INTERFACE (for backward compatibility)
    # ========================================================================
    
    def chat(self, message: str, user_id: Optional[str] = None) -> str:
        """
        Simple chat interface for backward compatibility.
        
        Args:
            message: User message
            user_id: Optional user ID
            
        Returns:
            Response string
        """
        result = self.process_query(query=message, user_id=user_id)
        return result["final_response"]


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_workflow_orchestrator() -> Orchestrator:
    """
    Factory function to create WorkflowOrchestrator instance.
    
    Returns:
        Configured WorkflowOrchestrator
    """
    return Orchestrator()


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    import logging
    logger.basicConfig(
        level=logger.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 70)
    print("Testing WorkflowOrchestrator")
    print("=" * 70)
    
    orchestrator = create_workflow_orchestrator()
    
    test_queries = [
        "Explain how probability works",
        "Generate a quiz on statistics",
        "Create slides about linear algebra",
        "Show me my performance report"
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}")
        
        result = orchestrator.process_query(query, user_id="test_user")
        
        print(f"Query Type: {result['query_type']}")
        print(f"Agents Used: {result['metadata']['agents_used']}")
        print(f"Duration: {result['metadata']['duration_ms']}ms")
        print(f"\nResponse:\n{result['final_response']}")
