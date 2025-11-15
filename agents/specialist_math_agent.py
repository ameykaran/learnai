"""Specialist Math Agent using LiquidAI LFM2-350M-Math finetuned model.

This agent wraps a HuggingFace transformers model as a Strands-compatible agent for mathematical problem solving.
"""
import logging
from strands.tools import tool

logger = logging.getLogger(__name__)

# Global model cache to avoid reloading
_MODEL_CACHE = {}


def _get_math_model():
    """Lazy load the math model and tokenizer (cached singleton)."""
    if "model" in _MODEL_CACHE:
        return _MODEL_CACHE["model"], _MODEL_CACHE["tokenizer"]
    
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        logger.info("Loading LiquidAI/LFM2-350M-Math model...")
        model_id = "LiquidAI/LFM2-350M-Math"
        
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            dtype="float32",
            # attn_implementation="flash_attention_2"  # uncomment if you have flash_attn
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        _MODEL_CACHE["model"] = model
        _MODEL_CACHE["tokenizer"] = tokenizer
        
        logger.info("Math model loaded successfully")
        return model, tokenizer
        
    except Exception as e:
        logger.exception("Failed to load math model: %s", e)
        raise


class SpecialistMathAgent:
    """Strands-compatible agent wrapper for the finetuned math model."""
    
    def __init__(
        self,
        model_id: str = "LiquidAI/LFM2-350M-Math",
        temperature: float = 0.6,
        top_p: float = 0.95,
        min_p: float = 0.1,
        repetition_penalty: float = 1.05,
        max_new_tokens: int = 1024,
    ):
        self.name = "specialist_math_agent"
        self.model_id = model_id
        self.temperature = temperature
        self.top_p = top_p
        self.min_p = min_p
        self.repetition_penalty = repetition_penalty
        self.max_new_tokens = max_new_tokens
        
        # Lazy load - model is loaded on first call
        self._model = None
        self._tokenizer = None
    
    def _ensure_loaded(self):
        """Ensure model and tokenizer are loaded."""
        if self._model is None or self._tokenizer is None:
            self._model, self._tokenizer = _get_math_model()
    
    def __call__(self, prompt: str, retrieved_docs: str = "") -> str:
        """Execute the math model on the given query.
        
        Args:
            prompt: The user's mathematical query
            retrieved_docs: Optional context from RAG retrieval
            
        Returns:
            Model's response as a string
        """
        self._ensure_loaded()
        
        # Combine query with retrieved context (fewshots/examples)
        if retrieved_docs:
            combined = (
                f"Help to solve the user's query in maximum 500 words:\n{prompt}\n\n"
                f"Some additional context that might help you:\n{retrieved_docs}"
            )
        else:
            combined = f"Help to solve the user's query:\n{prompt}"
        
        logger.info(f"[Specialist Agent] input: {combined[:100]}...{combined[-100:]}")
        
        try:
            # Create message in chat format
            message = [
                {"role": "user", "content": combined},
            ]
            
            # Tokenize with chat template
            input_ids = self._tokenizer.apply_chat_template(
                message,
                add_generation_prompt=True,
                return_tensors="pt",
                tokenize=True,
            ).to(self._model.device)
            
            logger.info("[Specialist Agent] input token count: %d", input_ids.shape[1])

            # Generate response
            output = self._model.generate(
                input_ids,
                do_sample=True,
                temperature=self.temperature,
                top_p=self.top_p,
                min_p=self.min_p,
                repetition_penalty=self.repetition_penalty,
                max_new_tokens=self.max_new_tokens,
            )
            
            # Decode output
            response = self._tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Extract only the assistant's response (remove the input prompt)
            # The chat template usually adds markers, so we try to extract the new content
            if "assistant" in response:
                response = response.split("assistant")[-1].strip()
            elif message[0]["content"] in response:
                response = response.replace(message[0]["content"], "").strip()

            logger.info("[Specialist Agent] response length: %d chars", len(response))
            logger.info(f"[Specialist Agent] output: {response[:100]}...{response[-100:]}")
            
            return response
            
        except Exception as e:
            logger.exception("Math model inference failed: %s", e)
            return f"[Specialist Agent] Error: Failed to generate response: {e}"


# Create a singleton instance
_specialist_math_agent_instance = None


def get_specialist_math_agent() -> SpecialistMathAgent:
    """Get or create the singleton math agent instance."""
    global _specialist_math_agent_instance
    if _specialist_math_agent_instance is None:
        _specialist_math_agent_instance = SpecialistMathAgent()
    return _specialist_math_agent_instance


@tool
def specialist_math_tool(query: str, retrieved_docs: str = "") -> str:
    """Specialist tool for mathematical problem solving using finetuned model.
    
    Args:
        query: The mathematical problem to solve
        retrieved_docs: Context from RAG retrieval (examples, similar problems)
    
    Returns:
        Solution with step-by-step working
    """
    agent = get_specialist_math_agent()
    return agent(query, retrieved_docs)


__all__ = ["SpecialistMathAgent", "get_specialist_math_agent", "specialist_math_tool"]
