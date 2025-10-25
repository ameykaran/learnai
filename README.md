# Probability SME Agent: Self-Adaptive Document Processing System

A self-adaptive agent Subject Matter Expert (SME) system for processing mathematical textbooks with dual-pipeline architecture and intelligent content extraction.

## Overview

This system implements a novel dual-pipeline approach that intelligently selects between Marker-based parsing and OCR-based processing based on document characteristics. Using the NCERT probability chapter as a proof-of-concept, it demonstrates robust handling of complex mathematical content including LaTeX formatting, images, tables, and graphs.

![AGENT2026-lma](https://github.com/user-attachments/assets/525eb135-af69-45a1-bbf7-93a522704fad)


## Key Features

- **Self-Adaptive Pipeline Selection**: Automatically chooses optimal processing method based on content density
- **Mathematical Notation Preservation**: Maintains LaTeX formatting and complex mathematical expressions
- **Structured Metadata Extraction**: Rich semantic annotations with educational content classification
- **Custom NER Model**: Trained on 500+ probability-related terms for keyword extraction
- **Hybrid RAG System**: Combines semantic search with metadata filtering for intelligent content retrieval
- **Cost Optimization**: 15-30% reduction in processing costs through adaptive token management

## Architecture

The system consists of two main processing pipelines:

1. **Marker-Based Pipeline**: Direct PDF processing with excellent structure preservation
2. **OCR-Based Pipeline**: Image-based processing with predictable token usage (888 tokens/page)

The self-adaptive processor analyzes document characteristics and routes content through the most efficient pipeline.


## Technology Stack

- **Language**: Python 3.8+
- **ML Framework**: DSPy for structured outputs
- **LLM**: Google Gemini 2.5 Flash
- **NLP**: SpaCy for NER, RapidFuzz for fuzzy matching
- **Document Processing**: Marker library
- **Parallel Processing**: ThreadPoolExecutor
- **Data Storage**: JSON for chunks, Hybrid RAG for retrieval

## Data Schema

Each processed chunk follows this structure:

```python
{
    "text": str,
    "metadata": {
        "source_url": str,
        "source_type": str,
        "topics": List[str],
        "subtopics": List[str],
        "chunk_type": Literal["definition", "example", "explanation",
                             "proof", "visualization", "practice_problem",
                             "worked_solution", "analogy", "misconception"],
        "difficulty_level": Literal["basic", "intermediate", "advanced"],
        "prerequisites": List[str]
    }
}
```

## Results

- **Token Efficiency**: 15-30% cost reduction through adaptive pipeline selection
- **Mathematical Preservation**: 95% accuracy in LaTeX formula extraction
- **NER Performance**: 91% accuracy in keyword extraction
- **Processing Speed**: Parallel processing with configurable worker threads

## Demo Output

```bash
Query: 'Explain the concept of conditional probability.'
Input Filters: {'topics': ['conditional probability', 'probability'],
                'chunk_type': 'explanation'}
Found 3 results.
Retrieved Chunks:

Source Type: textbook, Chunk Type: explanation
Content: ## 13.2.1 Properties of conditional probability...
Topics: ['conditional probability', 'properties of probability', 'sample space']
```

## Future Work

Post mid-evaluation deliverables will include:
- Core SME capabilities (quiz generation, dynamic learning modules)
- Conversational agents with multi-step reasoning workflows - Integration with MOYA
- Tool-using capabilities (document generation, email automation)
- Hybrid retrieval mechanisms combining vector search with BM25
- Guardrails for input sanitization and output moderation
- Modular API servers with FastAPI

## Research Context

This work builds upon the DeepSeek-OCR research findings, which demonstrated 97% OCR precision at 10× compression ratios. Our adaptive approach leverages these insights to optimize processing costs while maintaining mathematical accuracy.

## Future Integration

The current implementation serves as a proof-of-concept for integration with the MOYA multiagent framework - an engineering LLM-powered multiagent system for autonomous operations. MOYA will provide the architectural foundation for scaling this approach to handle diverse educational materials simultaneously.

## Contributors

- Sreemaee Akshathala (2025701028)
- Amey Karan (2022111026)
