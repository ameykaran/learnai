"""Query classification utilities for the orchestrator.

Provides a rule-based classifier plus an optional LLM-driven hook.
"""
from typing import Dict, Tuple, Optional
import logging
from strands import Agent

logger = logging.getLogger(__name__)


QUERY_TYPES: Dict[str, Dict] = {
    "concept_explanation": {
        "description": "Requests for explanations of concepts or topics.",
        "keywords": ["explain", "what is", "how does", "teach me", "understand"],
        "agents": ["retriever"],
        "workflow": "sequential",
    },
    "assessment": {
        "description": "Requests for quizzes or tests to assess knowledge.",
        "keywords": ["quiz", "test", "assess", "evaluate", "practice"],
        "agents": ["retriever", "quiz"],
        "workflow": "sequential",
    },
    "performance_report": {
        "description": "Requests for performance reports or analytics.",
        "keywords": ["performance", "progress", "report", "analytics", "dashboard"],
        "agents": ["report"],
        "workflow": "direct",
    },
    "domain_query": {
        "description": "Requests for general or domain-specific mathematical problem solving.",
        "keywords": ["solve", "calculate", "help with", "problem", "integrate", "derivative", 
                     "equation", "algebra", "geometry", "trigonometry", "calculus", "sum", 
                     "product", "prove", "find", "compute", "evaluate"],
        "agents": ["retriever", "specialist"],
        "workflow": "sequential",
    },
    "content_creation": {
        "description": "Requests for creating or generating new content.",
        "keywords": ["create", "generate", "make", "build", "design"],
        "agents": ["retriever", "content_generation"],
        "workflow": "sequential",
    },
}


class Classifier:
    """Simple classifier with rule-based scoring and optional LLM hook.

    Usage:
        qc = Classifier()
        best, scores = qc.classify("Explain how backpropagation works")
    """

    def __init__(self, query_types: Dict = None, llm_enabled: bool = True):
        self.query_types = query_types or QUERY_TYPES
        self.llm_enabled = llm_enabled
        self._classification_agent = None
        
        # Initialize LLM classification agent if enabled and Agent is available
        if self.llm_enabled:
            try:
                self._classification_agent = Agent(
                    name="query_classifier",
                    system_prompt="""You are a query classification expert. 
Classify user queries into exactly ONE of these categories:"""
+ "\n".join(f"- {cat}: {self.query_types[cat]['description']}" for cat in self.query_types.keys()) + """
Respond with ONLY the category name, nothing else.""",
                )
                logger.info("LLM classification enabled with Strands Agent")
            except Exception as e:
                logger.warning("Failed to initialize LLM classifier, will use rule-based: %s", e)
                self._classification_agent = None


    def classify_rule_based(self, query: str) -> Tuple[str, Dict[str, int]]:
        """Rule-based classification: returns best match and raw scores."""
        query_lower = query.lower()
        scores = {}

        for qtype, cfg in self.query_types.items():
            score = 0
            for kw in cfg.get("keywords", []):
                if kw in query_lower:
                    score += 1
            scores[qtype] = score

        # If all zero, return 'concept_explanation' as default fallback
        best = max(scores, key=scores.get)
        if scores.get(best, 0) == 0:
            best = "concept_explanation"

        logger.info(
            "rule_based_classification",
            extra={
                "extra_json": {"query": query, "best": best, "scores": scores}
            },
        )

        return best, scores

    def classify(self, query: str) -> Tuple[str, Dict[str, int]]:
        """Classify query using LLM if enabled, otherwise fall back to rule-based.
        
        Returns a tuple of (best_category, scores_dict) for consistency with
        rule-based classification.
        """
        # If LLM is enabled and available, try LLM classification first
        if self.llm_enabled and self._classification_agent is not None:
            prompt = (
                "Classify the following user query into one of these categories:\n"
                + ", ".join(self.query_types.keys())
                + "\n\nQuery: "
                + query
                + "\n\nCategory:"
            )

            logger.debug("LLM classification prompt: %s", prompt)

            try:
                choice = self._classification_agent(prompt)
                choice = str(choice).strip().lower()
                
                # Check if the response matches any category
                for category in self.query_types.keys():
                    if category in choice or choice in category:
                        logger.info(
                            "llm_classification_result",
                            extra={"extra_json": {"query": query, "llm_choice": category}},
                        )
                        # Return with empty scores dict to indicate LLM classification
                        return category, {"llm_classified": 1}
                
            except Exception as e:
                logger.exception("LLM classification failed: %s", e)

        # Fallback to rule-based classification
        logger.debug("Using rule-based classification for query: %s", query)
        best, scores = self.classify_rule_based(query)
        return best, scores


__all__ = ["QUERY_TYPES", "Classifier"]
