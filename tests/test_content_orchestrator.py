#!/usr/bin/env python3
"""
Test script for content generation agent integration with orchestrator.
"""

import logging
from agents.orchestrator.orchestrator import create_workflow_orchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_content_generation():
    """Test content generation through orchestrator."""
    print("=" * 70)
    print("Testing Content Generation Agent Integration")
    print("=" * 70)
    
    # Create orchestrator
    orchestrator = create_workflow_orchestrator()
    
    # Test queries for content generation
    test_queries = [
        # "Create a PDF document about probability theory",
        # "Generate slides about linear algebra",
        "Make a presentation on calculus basics",
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}")
        
        try:
            result = orchestrator.process_query(
                query=query,
                user_id="test_user_content"
            )
            
            print(f"\nQuery Type: {result['query_type']}")
            print(f"Agents Used: {result['metadata']['agents_used']}")
            print(f"Duration: {result['metadata']['duration_ms']}ms")
            print(f"\nResponse Preview:\n{result['final_response'][:500]}...")
            
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_content_generation()
