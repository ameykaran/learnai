#!/usr/bin/env python3
"""
CLI interface for testing the Onboarding Agent.
Run this to interact with the agent in the terminal.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import argparse
from agents.onboarding.agent import create_onboarding_agent
from agents.onboarding.config import OnboardingConfig
from agents.onboarding.prompts import USER_GREETING


def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print("  🎓 ONBOARDING AGENT - Adaptive Probability Assessment")
    print("=" * 70)
    print()


def print_separator():
    """Print separator line."""
    print("\n" + "-" * 70 + "\n")


def run_interactive_assessment(user_id: str, total_questions: int = None):
    """
    Run an interactive assessment session.
    
    Args:
        user_id: User identifier
        total_questions: Optional number of questions override
    """
    print_banner()
    
    # Create agent
    print("🔄 Initializing agent...")
    try:
        config = OnboardingConfig()
        agent = create_onboarding_agent(user_id=user_id, config=config)
        print("✅ Agent initialized successfully!\n")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Show greeting
    total_q = total_questions or config.DEFAULT_TOTAL_QUESTIONS
    print(USER_GREETING.format(total_questions=total_q))
    print_separator()
    
    # Start conversation loop
    print("💬 Chat with the agent (type 'quit' or 'exit' to end)\n")
    
    # Initial message to start
    initial_msg = f"I'm ready to start! My user ID is {user_id}."
    if total_questions:
        initial_msg += f" Please use {total_questions} questions."
    
    conversation_active = True
    
    try:
        # First interaction
        print(f"You: {initial_msg}\n")
        response = agent.chat(initial_msg)
        print(f"Agent: {response}\n")
        print_separator()
        
        # Continue conversation
        while conversation_active:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input or user_input is None:
                    continue
                
                print(f"User input: {user_input}")

                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'stop']:
                    print("\n👋 Goodbye! Your progress has been saved.")
                    break
                
                # Send to agent
                response = agent.chat(user_input)
                print(f"\nAgent: {response}\n")
                print_separator()
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Assessment interrupted. Your progress has been saved.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                continue
                
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return
    
    print("\n✅ Assessment session ended.")


def run_automated_demo(user_id: str):
    """
    Run an automated demo showing agent capabilities.
    
    Args:
        user_id: User identifier
    """
    print_banner()
    print("🤖 Running automated demo...\n")
    
    try:
        config = OnboardingConfig()
        agent = create_onboarding_agent(user_id=user_id, config=config)
        
        demo_messages = [
            f"Start assessment for user {user_id}",
            "Show me the first question",
            "I think the answer is A",
            "Get my current progress",
        ]
        
        for msg in demo_messages:
            print(f"📨 Sending: {msg}")
            response = agent.chat(msg)
            print(f"🤖 Response: {response}\n")
            print_separator()
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Onboarding Agent CLI - Adaptive Probability Assessment"
    )
    
    parser.add_argument(
        "--user-id",
        type=str,
        default="test_user_001",
        help="User identifier (default: test_user_001)"
    )
    
    parser.add_argument(
        "--questions",
        type=int,
        default=None,
        help="Number of questions (default: from environment or 25)"
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run automated demo instead of interactive mode"
    )
    
    args = parser.parse_args()
    
    # Run appropriate mode
    if args.demo:
        run_automated_demo(args.user_id)
    else:
        run_interactive_assessment(args.user_id, args.questions)


if __name__ == "__main__":
    main()
