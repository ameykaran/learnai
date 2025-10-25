"""Compatibility shim for the keyword extractor used across the project.

Expose KeywordExtractor name expected by existing imports by aliasing the
MathKeywordExtractor implemented in math_keyword_extractor.py.
"""

from .math_keyword_extractor import MathKeywordExtractor as KeywordExtractor

__all__ = ["KeywordExtractor"]
