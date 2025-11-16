"""Specialist Math Agent - Strands agent for mathematical problem solving.

This agent wraps a HuggingFace finetuned model (LFM2-350M-Math) as a Strands agent,
enabling sophisticated mathematical problem solving with step-by-step explanations.
"""
import logging
from typing import Optional
from strands import Agent

from agents.specialist.config import (
    AGENT_NAME,
    AGENT_DESCRIPTION,
    SYSTEM_PROMPT,
    MODEL_ID
)
from agents.specialist.tools import specialist_math_tools

logger = logging.getLogger(__name__)


class SpecialistMathAgent:
    """Specialist agent for advanced mathematical problem solving.
    
    This agent uses the LiquidAI LFM2-350M-Math model, which is specifically
    finetuned for mathematical reasoning and problem solving. It can handle:
    - Algebraic manipulations and equation solving
    - Calculus (derivatives, integrals, limits)
    - Probability and statistics
    - Geometry and trigonometry
    - Mathematical proofs
    - Word problems
    
    The agent integrates with the RAG system to leverage relevant examples
    and context from the knowledge base.
    
    Example:
        >>> agent = SpecialistMathAgent()
        >>> response = agent("Find the derivative of f(x) = x^3 + 2x")
        >>> print(response)
    """
    
    def __init__(
        self,
        model_id: str = MODEL_ID,
        temperature: float = 0.6,
    ):
        """Initialize the specialist math agent.
        
        Args:
            model_id: HuggingFace model ID (default: LFM2-350M-Math)
            temperature: Sampling temperature for generation (default: 0.6)
        """
        logger.info("=" * 60)
        logger.info("Initializing Specialist Math Agent")
        logger.info("Model: %s", model_id)
        logger.info("Temperature: %.2f", temperature)
        
        self.model_id = model_id
        self.temperature = temperature
        
        # Create the Strands agent with tools
        logger.info("Creating Strands agent with %d tools...", len(specialist_math_tools))
        try:
            self.agent = Agent(
                name=AGENT_NAME,
                system_prompt=SYSTEM_PROMPT,
                tools=specialist_math_tools,
            )
            logger.info("✓ Strands agent created successfully")
        except Exception as e:
            logger.error("✗ Failed to create Strands agent: %s", e)
            raise
        
        logger.info("=" * 60)
        logger.info("Specialist Math Agent ready")
        logger.info("=" * 60)
    
    def __call__(self, query: str, context: Optional[str] = None) -> str:
        """Process a mathematical problem query.
        
        Args:
            query: The mathematical problem or question to solve
            context: Optional context from RAG retrieval (examples, formulas, etc.)
        
        Returns:
            The agent's response with step-by-step solution
        """
        logger.info("=" * 60)
        logger.info("Processing query: %s", query[:100])
        
        # If context is provided, prepend it to the query
        if context:
            logger.info("Context provided: %d characters", len(context))
            enhanced_query = (
                f"I have some relevant context that might help:\n\n"
                f"{context}\n\n"
                f"Now, please help me with: {query}"
            )
        else:
            logger.info("No context provided, using query only")
            enhanced_query = query
        
        try:
            logger.info("Calling Strands agent...")
            response = self.agent(enhanced_query)
            logger.info("✓ Agent response received (%d chars)", len(str(response)))
            logger.info("=" * 60)
            return str(response)
            
        except Exception as e:
            logger.exception("Agent processing failed: %s", e)
            error_response = (
                f"I encountered an error while processing your question:\n\n"
                f"Error: {str(e)}\n\n"
                f"Please try rephrasing your question or breaking it down into simpler parts."
            )
            return error_response
    
    # def solve(self, problem: str, with_context: bool = False) -> str:
    #     """Convenience method to solve a mathematical problem.
        
    #     Args:
    #         problem: The mathematical problem to solve
    #         with_context: Whether to automatically retrieve context (not implemented yet)
        
    #     Returns:
    #         Solution with step-by-step working
    #     """
    #     return self(problem)
    
    def get_info(self) -> dict:
        """Get information about the agent.
        
        Returns:
            Dictionary containing agent metadata
        """
        return {
            "name": AGENT_NAME,
            "description": AGENT_DESCRIPTION,
            "model_id": self.model_id,
            "temperature": self.temperature,
            "tools": [tool.__name__ for tool in specialist_math_tools],
            "capabilities": [
                "Algebraic problem solving",
                "Calculus (derivatives, integrals, limits)",
                "Probability and statistics",
                "Geometry and trigonometry",
                "Mathematical proofs",
                "Word problems"
            ]
        }


# Singleton instance
_specialist_agent_instance = None


def get_specialist_agent(
    model_id: str = MODEL_ID,
    temperature: float = 0.6,
) -> SpecialistMathAgent:
    """Get or create the singleton specialist agent instance.
    
    Args:
        model_id: HuggingFace model ID
        temperature: Sampling temperature
    
    Returns:
        SpecialistMathAgent instance
    """
    global _specialist_agent_instance
    
    if _specialist_agent_instance is None:
        logger.info("Creating new specialist agent instance")
        _specialist_agent_instance = SpecialistMathAgent(
            model_id=model_id,
            temperature=temperature,
        )
    else:
        logger.info("Using existing specialist agent instance")
    
    return _specialist_agent_instance


__all__ = ["SpecialistMathAgent", "get_specialist_agent"]
