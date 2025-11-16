"""Configuration for the Specialist Math Agent."""
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_ID = "LiquidAI/LFM2-350M-Math"
MODEL_TEMPERATURE = 0.6
MODEL_TOP_P = 0.95
MODEL_MIN_P = 0.1
MODEL_REPETITION_PENALTY = 1.05
MODEL_MAX_NEW_TOKENS = 1024

# Agent configuration
AGENT_NAME = "specialist_math_agent"
AGENT_DESCRIPTION = "Expert mathematical problem solver using finetuned LFM2-350M-Math model"

# System prompt for the specialist agent
SYSTEM_PROMPT = """You are an expert mathematics tutor and problem solver. Your role is to:

1. **Solve mathematical problems** with clear, step-by-step explanations
2. **Use provided context** from the knowledge base to support your solutions
3. **Show your work** - explain each step of your reasoning
4. **Verify your answers** - double-check calculations when possible
5. **Provide insights** - explain why certain approaches work
6. **Connect concepts** - relate the problem to broader mathematical principles

When solving problems:
- Start by understanding what is being asked
- Identify relevant formulas, theorems, or concepts
- Work through the solution systematically
- Explain any non-obvious steps
- State your final answer clearly
- Suggest follow-up practice if relevant

Be clear, thorough, and educational in your approach."""

# Tool descriptions
SPECIALIST_TOOL_DESCRIPTION = """Solve complex mathematical problems using a finetuned model.

This tool is specifically designed for:
- Algebraic problem solving
- Calculus problems (derivatives, integrals, limits)
- Probability and statistics calculations
- Geometry and trigonometry
- Mathematical proofs and reasoning
- Word problems requiring mathematical modeling

The tool performs best when provided with:
1. Clear problem statement
2. Relevant context from the knowledge base (examples, similar problems)
"""

logger.info("Specialist agent configuration loaded: %s", MODEL_ID)
