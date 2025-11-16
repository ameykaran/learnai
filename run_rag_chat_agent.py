"""
Run the RAG Chat Agent - Interactive Educational Tutor

This script provides an interactive command-line interface to chat with
the RAG Chat Agent, an intelligent tutor for probability and statistics.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.retrieval import RAGChatAgent, RAGChatConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print("  RAG CHAT AGENT - Intelligent Tutor for Probability & Statistics")
    print("=" * 70)
    print("\nThis agent uses retrieval-augmented generation to provide accurate,")
    print("high-quality educational content. It can:")
    print("  • Explain concepts with definitions and examples")
    print("  • Provide practice problems and worked solutions")
    print("  • Show visualizations and analogies")
    print("  • Identify prerequisites and related topics")
    print("  • Clarify common misconceptions")
    print("\nType 'exit' or 'quit' to end the conversation.")
    print("Type 'help' for tips on how to interact with the agent.")
    print("=" * 70 + "\n")


def print_help():
    """Print help message."""
    help_text = """
TIPS FOR INTERACTING WITH THE AGENT:
====================================

Ask natural questions:
  • "What is conditional probability?"
  • "Can you explain Bayes theorem?"
  • "I don't understand independence"

Request specific content types:
  • "Give me an example of probability distributions"
  • "Show me a practice problem about expected value"
  • "Can you provide an analogy for random variables?"

Explore related concepts:
  • "What topics are related to Bayes theorem?"
  • "What do I need to learn before studying hypothesis testing?"

Get practice:
  • "Give me a problem to solve"
  • "Can you show me how to solve that?"
  • "I need more practice with probability"

The agent will automatically:
  - Extract key topics from your questions
  - Determine the best content type to retrieve
  - Provide pedagogically sound explanations
  - Adapt to your learning needs

Just ask naturally, and the agent will guide you!
"""
    print(help_text)


def run_interactive_session():
    """Run an interactive chat session with the agent."""
    
    print_banner()
    
    try:
        # Initialize agent
        print("Initializing agent... (this may take a moment)\n")
        config = RAGChatConfig()
        agent = RAGChatAgent(config=config)
        
        # Print welcome message
        print("\n" + "=" * 70)
        print(agent.welcome())
        print("=" * 70 + "\n")
        
        # Start conversation loop
        conversation_count = 0
        
        while True:
            try:
                # Get user input
                user_input = input("\n🎓 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n👋 Thank you for learning with me! Goodbye!\n")
                    break
                
                # Check for help
                if user_input.lower() == 'help':
                    print_help()
                    continue
                
                # Check for empty input
                if not user_input:
                    print("Please ask a question or type 'help' for tips.")
                    continue
                
                # Get agent response
                print("\n🤖 Agent: ", end="", flush=True)
                response = agent.chat(user_input)
                print(response)
                
                conversation_count += 1
                
                # Offer stats after several interactions
                if conversation_count == 5:
                    print("\n💡 Tip: You can ask 'What topics do you cover?' to see what's available in the knowledge base.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Conversation interrupted. Goodbye!\n")
                break
            except Exception as e:
                logger.error(f"Error during conversation: {e}")
                print(f"\n❌ Sorry, I encountered an error: {e}")
                print("Let's try again. Please rephrase your question.")
    
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        print(f"\n❌ Failed to initialize agent: {e}")
        print("\nPlease check:")
        print("  1. AWS credentials are configured")
        print("  2. Required environment variables are set")
        print("  3. Knowledge base exists at the configured path")
        print("  4. All dependencies are installed")
        sys.exit(1)


def run_single_query(query: str):
    """Run a single query and exit."""
    try:
        print(f"Initializing agent...\n")
        config = RAGChatConfig()
        agent = RAGChatAgent(config=config)
        
        print(f"Query: {query}\n")
        response = agent.chat(query)
        print(f"Response:\n{response}\n")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        run_single_query(query)
    else:
        # Interactive mode
        run_interactive_session()


if __name__ == "__main__":
    main()
