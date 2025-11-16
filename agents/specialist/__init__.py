"""Specialist Math Agent - Advanced mathematical problem solving using finetuned models.

This agent uses the LiquidAI LFM2-350M-Math model to solve complex mathematical problems,
leveraging context from the RAG system for improved accuracy.
"""

from agents.specialist.agent import SpecialistMathAgent, get_specialist_agent
from agents.specialist.tools import specialist_math_tools

__all__ = ["SpecialistMathAgent", "get_specialist_agent", "specialist_math_tools"]
