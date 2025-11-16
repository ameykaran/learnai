"""Tools for the Specialist Math Agent.

These tools wrap the HuggingFace transformers model for mathematical problem solving.
"""
import logging
from typing import Optional
from strands import tool

logger = logging.getLogger(__name__)

# Global model cache to avoid reloading
_MODEL_CACHE = {}


def _get_math_model():
    """Lazy load the math model and tokenizer (cached singleton)."""
    if "model" in _MODEL_CACHE:
        logger.info("Using cached math model")
        return _MODEL_CACHE["model"], _MODEL_CACHE["tokenizer"]
    
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        logger.info("=" * 60)
        logger.info("Loading LiquidAI/LFM2-350M-Math model...")
        logger.info("This may take a few minutes on first load...")
        
        model_id = "LiquidAI/LFM2-350M-Math"
        
        logger.info("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        logger.info("✓ Tokenizer loaded")
  
        logger.info("Loading LiquidAI/LFM2-350M-Math model...")
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            dtype="float32",
            # attn_implementation="flash_attention_2"  # uncomment if you have flash_attn
        )
        logger.info("✓ Model loaded successfully")
        
        _MODEL_CACHE["model"] = model
        _MODEL_CACHE["tokenizer"] = tokenizer
        
        logger.info("=" * 60)
        logger.info("Math model ready for inference")
        logger.info("=" * 60)
        
        return model, tokenizer
        
    except ImportError as e:
        logger.error("Failed to import transformers. Please install: pip install transformers torch")
        raise ImportError(
            "transformers library not found. Install with: pip install transformers torch"
        ) from e
    except Exception as e:
        logger.exception("Failed to load math model: %s", e)
        raise


@tool
def solve_math_problem(
    problem: str,
    context: Optional[str] = None,
    max_tokens: int = 1024
) -> str:
    """Solve a mathematical problem using a finetuned language model.
    
    This tool uses the LiquidAI LFM2-350M-Math model, which is specifically
    finetuned for mathematical problem solving. It excels at:
    - Step-by-step algebraic manipulations
    - Calculus problems (derivatives, integrals, limits)
    - Probability and statistics calculations
    - Geometry and trigonometry
    - Mathematical proofs and logical reasoning
    - Word problems requiring mathematical modeling
    
    Args:
        problem: The mathematical problem to solve. Be specific and clear.
                Example: "Find the derivative of f(x) = x^3 + 2x^2 - 5x + 3"
                Example: "A bag contains 3 red balls and 5 blue balls. What is 
                         the probability of drawing 2 red balls without replacement?"
        context: Optional context from the knowledge base that might help solve
                the problem. This can include similar examples, relevant formulas,
                or theoretical background.
        max_tokens: Maximum number of tokens to generate (default: 1024)
    
    Returns:
        A detailed solution with step-by-step working and explanations
    
    Examples:
        # Simple algebra
        solve_math_problem("Solve for x: 2x + 5 = 13")
        
        # With context
        solve_math_problem(
            "Find P(A|B) if P(A) = 0.3, P(B) = 0.4, and P(A∩B) = 0.12",
            context="Bayes theorem: P(A|B) = P(A∩B) / P(B)"
        )
        
        # Calculus
        solve_math_problem("Integrate: ∫(3x^2 + 2x) dx")
    """
    logger.info("=" * 60)
    logger.info("SOLVE_MATH_PROBLEM Tool Called")
    logger.info("Problem: %s", problem[:200])
    if context:
        logger.info("Context provided: %d characters", len(context))
    
    try:
        # Load model (lazy loading with caching)
        model, tokenizer = _get_math_model()
        
        # Build the prompt
        if context:
            combined_input = (
                f"You are solving a mathematical problem. Here is some relevant context:\n\n"
                f"{context}\n\n"
                f"Now solve this problem:\n{problem}\n\n"
                f"Provide a clear, step-by-step solution:"
            )
        else:
            combined_input = (
                f"Solve this mathematical problem with clear step-by-step working:\n\n"
                f"{problem}"
            )
        
        logger.info("Combined input length: %d characters: %s...", len(combined_input), combined_input[:100])
        logger.debug("Full input: %s", combined_input)
        
        # Create message in chat format
        message = [
            {"role": "user", "content": combined_input},
        ]
        
        # Tokenize with chat template
        logger.info("Tokenizing input...")
        input_ids = tokenizer.apply_chat_template(
            message,
            add_generation_prompt=True,
            return_tensors="pt",
            tokenize=True,
        ).to(model.device)
        
        logger.info("Input token count: %d", input_ids.shape[1])
        
        # Generate response
        logger.info("Generating solution...")
        output = model.generate(
            input_ids,
            do_sample=True,
            temperature=0.6,
            top_p=0.95,
            min_p=0.1,
            repetition_penalty=1.05,
            max_new_tokens=max_tokens,
        )
        
        # Decode output
        logger.info("Decoding output...")
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Extract only the assistant's response (remove the input prompt)
        # The chat template usually adds markers, so we extract the new content
        if "assistant" in response.lower():
            # Find the last occurrence of assistant marker
            parts = response.lower().split("assistant")
            if len(parts) > 1:
                response = response[response.lower().rfind("assistant") + len("assistant"):].strip()
        
        # Remove the original prompt if it's still there
        if combined_input in response:
            response = response.replace(combined_input, "").strip()
        
        logger.info("Generated solution length: %d characters", len(response))
        logger.info("Solution preview: %s...", response[:100])
        logger.info("=" * 60)
        
        return response
        
    except Exception as e:
        logger.exception("Math problem solving failed: %s", e)
        error_msg = (
            f"I encountered an error while trying to solve this problem:\n\n"
            f"Error: {str(e)}\n\n"
            f"Please try:\n"
            f"1. Rephrasing the problem more clearly\n"
            f"2. Breaking it down into smaller steps\n"
            f"3. Checking if the problem statement is complete"
        )
        return error_msg


@tool
def verify_solution(problem: str, solution: str) -> str:
    """Verify a mathematical solution by checking the steps and logic.
    
    This tool takes a problem and its proposed solution, then verifies
    whether the solution is correct and logically sound.
    
    Args:
        problem: The original mathematical problem
        solution: The proposed solution to verify
    
    Returns:
        Verification analysis with feedback on correctness
    
    Example:
        verify_solution(
            "Solve: 2x + 3 = 11",
            "2x = 8, so x = 4"
        )
    """
    logger.info("=" * 60)
    logger.info("VERIFY_SOLUTION Tool Called")
    logger.info("Problem: %s", problem[:100])
    logger.info("Solution to verify: %s", solution[:100])
    
    try:
        model, tokenizer = _get_math_model()
        
        verification_prompt = (
            f"Verify the following mathematical solution:\n\n"
            f"Problem: {problem}\n\n"
            f"Proposed Solution:\n{solution}\n\n"
            f"Is this solution correct? Check each step carefully and provide feedback:"
        )
        
        message = [{"role": "user", "content": verification_prompt}]
        
        input_ids = tokenizer.apply_chat_template(
            message,
            add_generation_prompt=True,
            return_tensors="pt",
            tokenize=True,
        ).to(model.device)
        
        logger.info("Generating verification...")
        output = model.generate(
            input_ids,
            do_sample=True,
            temperature=0.3,  # Lower temperature for more focused verification
            top_p=0.9,
            max_new_tokens=512,
        )
        
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Clean up response
        if "assistant" in response.lower():
            parts = response.lower().split("assistant")
            if len(parts) > 1:
                response = response[response.lower().rfind("assistant") + len("assistant"):].strip()
        
        if verification_prompt in response:
            response = response.replace(verification_prompt, "").strip()
        
        logger.info("Verification complete")
        logger.info("=" * 60)
        
        return response
        
    except Exception as e:
        logger.exception("Solution verification failed: %s", e)
        return f"Unable to verify solution due to error: {str(e)}"


# Export tools list
specialist_math_tools = [
    solve_math_problem,
    verify_solution
]

__all__ = ["solve_math_problem", "verify_solution", "specialist_math_tools"]
