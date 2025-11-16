#!/usr/bin/env python3
"""Test script for the Specialist Math Agent.

This script runs a series of tests to verify the specialist agent's functionality.
"""
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.specialist import get_specialist_agent
from agents.specialist.tools import solve_math_problem, verify_solution

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_tool_solve_math_problem():
    """Test the solve_math_problem tool directly."""
    print("\n" + "=" * 70)
    print("TEST 1: solve_math_problem Tool")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "Simple linear equation",
            "problem": "Solve for x: 2x + 5 = 13",
            "context": None
        },
        {
            "name": "Quadratic equation",
            "problem": "Solve: x^2 - 5x + 6 = 0",
            "context": "Hint: Try factoring or use the quadratic formula"
        },
        {
            "name": "Basic derivative",
            "problem": "Find d/dx of f(x) = x^3",
            "context": "Power rule: d/dx(x^n) = n*x^(n-1)"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test['name']} ---")
        print(f"Problem: {test['problem']}")
        if test['context']:
            print(f"Context: {test['context']}")
        
        try:
            result = solve_math_problem(
                problem=test['problem'],
                context=test['context']
            )
            print(f"✓ Result ({len(result)} chars):")
            print(result[:200] + "..." if len(result) > 200 else result)
        except Exception as e:
            print(f"✗ Error: {e}")
            logger.exception("Test failed")
    
    print("\n" + "=" * 70)


def test_tool_verify_solution():
    """Test the verify_solution tool."""
    print("\n" + "=" * 70)
    print("TEST 2: verify_solution Tool")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "Correct solution",
            "problem": "Solve: 2x + 3 = 11",
            "solution": "2x = 8, therefore x = 4"
        },
        {
            "name": "Incorrect solution",
            "problem": "Solve: 3x - 5 = 10",
            "solution": "3x = 15, therefore x = 4"  # Wrong!
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test['name']} ---")
        print(f"Problem: {test['problem']}")
        print(f"Solution: {test['solution']}")
        
        try:
            result = verify_solution(
                problem=test['problem'],
                solution=test['solution']
            )
            print(f"✓ Verification ({len(result)} chars):")
            print(result[:200] + "..." if len(result) > 200 else result)
        except Exception as e:
            print(f"✗ Error: {e}")
            logger.exception("Test failed")
    
    print("\n" + "=" * 70)


def test_agent_basic():
    """Test basic agent functionality."""
    print("\n" + "=" * 70)
    print("TEST 3: Agent Basic Functionality")
    print("=" * 70)
    
    try:
        print("\nInitializing agent...")
        agent = get_specialist_agent()
        print("✓ Agent initialized successfully")
        
        # Test agent info
        print("\nAgent information:")
        info = agent.get_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Test simple query
        print("\nTesting simple query...")
        problem = "What is 5 * 8?"
        print(f"Problem: {problem}")
        
        response = agent(problem)
        print(f"✓ Response received ({len(response)} chars):")
        print(response[:200] + "..." if len(response) > 200 else response)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        logger.exception("Test failed")
    
    print("\n" + "=" * 70)


def test_agent_with_context():
    """Test agent with context."""
    print("\n" + "=" * 70)
    print("TEST 4: Agent with Context")
    print("=" * 70)
    
    try:
        agent = get_specialist_agent()
        
        context = """
        Pythagorean Theorem: In a right triangle, a² + b² = c²
        where c is the hypotenuse and a, b are the other two sides.
        
        Example: If a = 3 and b = 4, then c² = 9 + 16 = 25, so c = 5
        """
        
        problem = "A right triangle has sides of length 6 and 8. Find the hypotenuse."
        
        print(f"Problem: {problem}")
        print(f"Context: {context[:100]}...")
        
        response = agent(problem, context=context)
        print(f"✓ Response received ({len(response)} chars):")
        print(response[:200] + "..." if len(response) > 200 else response)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        logger.exception("Test failed")
    
    print("\n" + "=" * 70)


def test_agent_complex_problem():
    """Test agent with a more complex problem."""
    print("\n" + "=" * 70)
    print("TEST 5: Complex Problem")
    print("=" * 70)
    
    try:
        agent = get_specialist_agent()
        
        problem = """
        A bag contains 5 red marbles and 7 blue marbles. If you draw 2 marbles
        without replacement, what is the probability that both are red?
        """
        
        print(f"Problem: {problem.strip()}")
        
        response = agent(problem)
        print(f"✓ Response received ({len(response)} chars):")
        print(response)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        logger.exception("Test failed")
    
    print("\n" + "=" * 70)


def run_all_tests():
    """Run all tests."""
    print("\n" + "🧪" * 35)
    print(" " * 20 + "SPECIALIST AGENT TESTS")
    print("🧪" * 35)
    
    tests = [
        ("Tool: solve_math_problem", test_tool_solve_math_problem),
        ("Tool: verify_solution", test_tool_verify_solution),
        ("Agent: Basic Functionality", test_agent_basic),
        ("Agent: With Context", test_agent_with_context),
        ("Agent: Complex Problem", test_agent_complex_problem),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n\nRunning: {name}")
        try:
            test_func()
            passed += 1
            print(f"✅ {name} PASSED")
        except Exception as e:
            failed += 1
            print(f"❌ {name} FAILED: {e}")
            logger.exception(f"Test {name} failed")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


def main():
    """Main function."""
    print("\nSpecialist Math Agent Test Suite")
    print("=" * 70)
    
    # Check if specific test is requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        tests = {
            "tool-solve": test_tool_solve_math_problem,
            "tool-verify": test_tool_verify_solution,
            "agent-basic": test_agent_basic,
            "agent-context": test_agent_with_context,
            "agent-complex": test_agent_complex_problem,
        }
        
        if test_name in tests:
            print(f"\nRunning single test: {test_name}")
            tests[test_name]()
            return 0
        else:
            print(f"Unknown test: {test_name}")
            print(f"Available tests: {', '.join(tests.keys())}")
            return 1
    
    # Run all tests
    return run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
