"""
Updated API Server Handler for Workflow Orchestrator
Drop-in replacement for handle_orchestrator in api_server/main.py
"""

import logging
from typing import Tuple, Dict, Any
from shared.models import UserProfile
from agents.orchestrator.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


async def handle_workflow_orchestrator(
    user_id: str,
    message: str,
    session: dict,
    orchestrator: Orchestrator,
    session_manager
) -> Tuple[str, Dict[str, Any]]:
    """
    Enhanced orchestrator handler using WorkflowOrchestrator.
    
    Args:
        user_id: User identifier
        message: User's message
        session: Session dict from session manager
        orchestrator: WorkflowOrchestrator instance
        session_manager: Session manager instance
        
    Returns:
        Tuple of (response_text, metadata_dict)
    """
    # Check if user has completed onboarding
    profile = session_manager.get_profile(user_id)
    
    if not profile:
        return (
            "Welcome! To get started, you'll need to complete a brief assessment. "
            "Would you like to begin the onboarding process?",
            {
                "agent": "Orchestrator",
                "needs_onboarding": True,
                "query_type": "onboarding_required"
            }
        )
    
    # Ensure profile is loaded in orchestrator
    orchestrator.store_profile(user_id, profile)
    
    # Build context from conversation history
    context = _build_context_from_history(session.get("conversation_history", []))
    
    try:
        # Process query through workflow orchestrator
        result = orchestrator.process_query(
            query=message,
            user_id=user_id,
            context=context
        )
        
        # Extract response and build metadata
        response_text = result["final_response"]
        metadata = {
            "agent": "Orchestrator",
            "query_type": result["query_type"],
            "classification_scores": result["scores"],
            "agents_used": result["metadata"]["agents_used"],
            "duration_ms": result["metadata"]["duration_ms"],
            "workflow": result["metadata"]["workflow"],
            "success": True
        }
        
        # Add step details for debugging (optional)
        if logger.isEnabledFor(logging.DEBUG):
            metadata["steps"] = [
                {
                    "agent": step["agent"],
                    "success": step.get("success", False),
                    "duration_ms": step.get("duration_ms", 0)
                }
                for step in result["steps"]
            ]
        
        logger.info(
            f"Orchestrator processed query successfully: "
            f"type={result['query_type']}, "
            f"agents={result['metadata']['agents_used']}, "
            f"duration={result['metadata']['duration_ms']}ms"
        )
        
        return response_text, metadata
        
    except Exception as exc:
        logger.error(f"Orchestrator error for user {user_id}: {exc}", exc_info=True)
        return (
            "I encountered an error processing your request. Please try again or rephrase your question.",
            {
                "agent": "Orchestrator",
                "error": str(exc),
                "success": False
            }
        )


def _build_context_from_history(
    conversation_history: list,
    max_messages: int = 5
) -> str:
    """
    Build context string from recent conversation history.
    
    Args:
        conversation_history: List of conversation messages
        max_messages: Maximum number of recent messages to include
        
    Returns:
        Context string
    """
    if not conversation_history:
        return ""
    
    # Get last N messages (excluding current)
    recent = conversation_history[-max_messages:]
    
    context_parts = []
    for msg in recent:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        if role == "user":
            context_parts.append(f"Previous user query: {content}")
        elif role == "assistant":
            # Truncate assistant responses to avoid context bloat
            truncated = content[:200] + "..." if len(content) > 200 else content
            context_parts.append(f"Previous response: {truncated}")
    
    return "\n".join(context_parts)

