#!/usr/bin/env python3
"""Example script to run the Specialist Math Agent.

This script demonstrates how to use the specialist agent for solving
mathematical problems, with and without context from the RAG system.
"""
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.specialist import get_specialist_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_usage():
    """Example 1: Basic usage without context."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Mathematical Problem Solving")
    print("=" * 70)
    
    agent = get_specialist_agent()
    
    problems = [
        "Solve for x: 2x + 5 = 13",
        "Find the derivative of f(x) = x^3 + 2x^2 - 5x + 3",
        "Calculate the integral: ∫(3x^2 + 2x) dx",
    ]
    
    for i, problem in enumerate(problems, 1):
        print(f"\n--- Problem {i} ---")
        print(f"Q: {problem}")
        print(f"\nA: ", end="")
        
        try:
            response = agent(problem)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 70)


def example_with_context():
    """Example 2: Using context from the knowledge base."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Problem Solving with Context")
    print("=" * 70)
    
    agent = get_specialist_agent()
    
    # Simulate context from RAG system
    context = """
    Conditional Probability Formula:
    P(A|B) = P(A ∩ B) / P(B)
    
    Where:
    - P(A|B) is the probability of A given B
    - P(A ∩ B) is the probability of both A and B occurring
    - P(B) is the probability of B occurring
    
    Example: If P(Rain) = 0.3, P(Cloud) = 0.5, and P(Rain ∩ Cloud) = 0.25,
    then P(Rain|Cloud) = 0.25 / 0.5 = 0.5
    """
    
    problem = """
    A medical test for a disease is 95% accurate. The disease affects 1% of the population.
    If a person tests positive, what is the probability they actually have the disease?
    """
    
    print(f"Problem:\n{problem}")
    print(f"\nContext provided:\n{context[:200]}...")
    print(f"\nSolution:")
    
    try:
        response = agent(problem, context=context)
        print(response)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)


def example_probability():
    """Example 3: Probability problems."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Probability and Statistics")
    print("=" * 70)
    
    agent = get_specialist_agent()
    
    problem = """
    A bag contains 5 red balls and 3 blue balls. If we draw 2 balls 
    without replacement, what is the probability that:
    a) Both balls are red?
    b) At least one ball is blue?
    """
    
    print(f"Problem:\n{problem}")
    print(f"\nSolution:")
    
    try:
        response = agent(problem)
        print(response)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)


def example_calculus():
    """Example 4: Calculus problems."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Calculus")
    print("=" * 70)
    
    agent = get_specialist_agent()
    
    problems = [
        {
            "problem": "Find the derivative of y = (3x^2 + 1)^5 using the chain rule",
            "context": "Chain Rule: If y = f(g(x)), then dy/dx = f'(g(x)) · g'(x)"
        },
        {
            "problem": "Evaluate the definite integral: ∫[0 to 2] (x^2 + 3) dx",
            "context": "Fundamental Theorem of Calculus: ∫[a to b] f(x)dx = F(b) - F(a)"
        }
    ]
    
    for i, item in enumerate(problems, 1):
        print(f"\n--- Problem {i} ---")
        print(f"Q: {item['problem']}")
        print(f"Context: {item['context']}")
        print(f"\nA: ", end="")
        
        try:
            response = agent(item['problem'], context=item['context'])
            print(response)
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 70)


def interactive_mode():
    """Interactive mode for testing the agent."""
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE - Specialist Math Agent")
    print("=" * 70)
    print("Type your mathematical problems. Type 'quit' or 'exit' to stop.")
    print("Type 'help' for usage tips.")
    print("=" * 70)
    
    agent = get_specialist_agent()
    
    while True:
        try:
            print("\n" + "-" * 70)
            user_input = input("\n🧮 Problem: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("""
Usage Tips:
- Type mathematical problems in plain text
- Use ^ for exponents (e.g., x^2 for x²)
- Use clear notation (e.g., "integral of x^2" or "∫x^2 dx")
- For fractions, use / (e.g., 1/2)
- Be specific about what you want (solve, find, calculate, etc.)

Examples:
- "Solve for x: 3x + 7 = 22"
- "Find the derivative of sin(2x)"
- "What is the probability of getting 2 heads in 3 coin flips?"
- "Integrate: ∫(x^2 + 3x) dx"
                """)
                continue
            
            print(f"\n🤖 Solution:")
            response = agent(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.exception("Error in interactive mode: %s", e)
            print(f"\n❌ Error: {e}")


def main():
    """Main function to run examples."""
    print("\n" + "🔬" * 35)
    print(" " * 20 + "SPECIALIST MATH AGENT")
    print(" " * 15 + "Mathematical Problem Solving Examples")
    print("🔬" * 35)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        print("\nRunning examples...")
        print("(Use --interactive flag for interactive mode)")
        
        try:
            example_basic_usage()
            example_probability()
            example_calculus()
            example_with_context()
            
            print("\n" + "=" * 70)
            print("✅ All examples completed!")
            print("=" * 70)
            print("\nTo try interactive mode, run:")
            print("  python run_specialist_agent.py --interactive")
            
        except Exception as e:
            logger.exception("Error running examples: %s", e)
            print(f"\n❌ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure transformers and torch are installed:")
            print("   pip install transformers torch")
            print("2. Check that you have enough disk space for the model (~1.4GB)")
            print("3. Ensure you have internet connection for first-time model download")


if __name__ == "__main__":
    main()
