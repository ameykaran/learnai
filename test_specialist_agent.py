"""Test script for the specialist math agent."""
import logging
from agents.utils import setup_logging
from agents.orchestrator import Orchestrator

def main():
    # Setup logging
    setup_logging(level=logging.INFO)
    
    # Create orchestrator
    orch = Orchestrator()
    
    # Test math queries
    math_queries = [
        # "Solve this calculus problem: integrate x^2",
        # "Find the derivative of sin(x)",
        # "What is the sum of 1 + 2 + 3 + ... + 100?",
        "Prove that the square root of 2 is irrational",
    ]
    
    print("\n" + "=" * 80)
    print("Testing Specialist Math Agent")
    print("=" * 80)
    
    for query in math_queries:
        print("\n" + "-" * 80)
        print(f"Query: {query}")
        print("-" * 80)
        
        try:
            result = orch.process_query(query, user_id="test_user")
            
            print(f"\nClassified as: {result['query_type']}")
            print(f"Classification scores: {result['scores']}")
            print(f"\nAgent steps:")
            for step in result['steps']:
                print(f"  - {step['agent']}: {step['output'][:200]}...")
            
            print(f"\n{'='*80}")
            print("Final Response:")
            print("="*80)
            print(result['final_response'])
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n")

if __name__ == "__main__":
    main()
