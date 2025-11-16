# Quick Start Guide - RAG Chat Agent

## Installation

Ensure you have all dependencies:

```bash
pip install strands chromadb dspy-ai sentence-transformers spacy rapidfuzz boto3 python-dotenv
```

## Setup

1. **Configure AWS Credentials** (for Bedrock access)
   ```bash
   aws configure
   ```

2. **Set Environment Variables** (optional - defaults provided)
   ```bash
   export AWS_REGION=us-east-1
   export BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
   export RAG_DB_PATH=./rag/prob_db
   ```

3. **Verify Knowledge Base Exists**
   ```bash
   # Check if database exists
   ls -la ./rag/prob_db/
   ```

## Quick Test

Run the test script to verify everything works:

```bash
python test_rag_chat_agent.py
```

Expected output:
```
✅ Agent created successfully!
✅ Welcome message retrieved successfully!
✅ Query processed successfully!
🎉 All tests passed!
```

## Interactive Usage

Launch the interactive chat interface:

```bash
python run_rag_chat_agent.py
```

Example session:
```
You: What is conditional probability?
Agent: [Retrieves definition and explains clearly]

You: Can you show me an example?
Agent: [Retrieves and presents a concrete example]

You: Give me a practice problem
Agent: [Presents a practice problem]
```

## Programmatic Usage

### Basic Example

```python
from agents.rag_chat import RAGChatAgent

# Create agent
agent = RAGChatAgent()

# Chat
response = agent.chat("What is conditional probability?")
print(response)
```

### Advanced Example

```python
from agents.rag_chat import RAGChatAgent, RAGChatConfig

# Custom configuration
config = RAGChatConfig()
config.DEFAULT_K = 5  # Retrieve more results

# Create agent
agent = RAGChatAgent(config=config)

# Welcome message
print(agent.welcome())

# Conversation
questions = [
    "What is Bayes theorem?",
    "Can you show me an example?",
    "What are the prerequisites?",
    "Give me a practice problem"
]

for question in questions:
    response = agent.chat(question)
    print(f"\nQ: {question}")
    print(f"A: {response}\n")
```

### Async Usage

```python
import asyncio
from agents.rag_chat import RAGChatAgent

async def main():
    agent = RAGChatAgent()
    
    # Multiple concurrent queries
    tasks = [
        agent.chat_async("What is probability?"),
        agent.chat_async("What is statistics?"),
        agent.chat_async("What is conditional probability?")
    ]
    
    responses = await asyncio.gather(*tasks)
    for i, response in enumerate(responses, 1):
        print(f"\nResponse {i}:\n{response}\n")

asyncio.run(main())
```

## Example Queries

### Getting Definitions
```python
agent.chat("What is conditional probability?")
agent.chat("Define random variable")
agent.chat("What does independence mean in probability?")
```

### Getting Examples
```python
agent.chat("Show me an example of Bayes theorem")
agent.chat("Give me a concrete example of probability distributions")
agent.chat("Can you demonstrate the law of total probability?")
```

### Getting Practice Problems
```python
agent.chat("Give me a probability problem to solve")
agent.chat("Can you give me practice with conditional probability?")
agent.chat("I want to practice Bayes theorem")
```

### Understanding Prerequisites
```python
agent.chat("What do I need to know before studying Bayes theorem?")
agent.chat("What are the prerequisites for hypothesis testing?")
agent.chat("I'm struggling with conditional probability - what should I learn first?")
```

### Exploring Related Topics
```python
agent.chat("What topics are related to probability distributions?")
agent.chat("What should I learn next after mastering basic probability?")
```

## Troubleshooting

### Error: "Failed to initialize agent"
**Solution:** 
- Check AWS credentials: `aws sts get-caller-identity`
- Verify Bedrock model access in your region
- Check environment variables are set

### Error: "No content found"
**Solution:**
- Verify knowledge base exists: `ls ./rag/prob_db/`
- Check database has content: Run test script
- Try broader search terms

### Slow Responses
**Solution:**
- First query is slower (model loading)
- Subsequent queries should be faster
- Use async for concurrent queries
- Reduce `DEFAULT_K` value

### Import Errors
**Solution:**
```bash
pip install strands chromadb dspy-ai sentence-transformers spacy rapidfuzz boto3
```

## Tips for Best Results

1. **Ask Natural Questions**
   - ✅ "What is conditional probability?"
   - ✅ "I don't understand Bayes theorem"
   - ✅ "Can you help me with probability distributions?"

2. **Be Specific About Content Type** (optional)
   - "Show me an **example** of..."
   - "Give me the **definition** of..."
   - "I need a **practice problem** for..."

3. **Follow Up Naturally**
   - The agent remembers context
   - "Can you explain that more simply?"
   - "Show me another example"
   - "What about the prerequisites?"

4. **Explore Related Concepts**
   - "What else should I learn?"
   - "How does this relate to X?"
   - "What topics are connected?"

## Integration Examples

### With Orchestrator

```python
from agents.orchestrator import Orchestrator
from agents.rag_chat import RAGChatAgent

orchestrator = Orchestrator()
rag_agent = RAGChatAgent()

orchestrator.add_agent("tutor", rag_agent)

response = orchestrator.route_query(
    "Explain conditional probability",
    preferred_agent="tutor"
)
```

### In a Web Application

```python
from fastapi import FastAPI
from agents.rag_chat import RAGChatAgent

app = FastAPI()
agent = RAGChatAgent()

@app.post("/chat")
async def chat(query: str):
    response = await agent.chat_async(query)
    return {"response": response}
```

### With Conversation History

```python
agent = RAGChatAgent()

conversation = [
    "What is probability?",
    "Can you give me an example?",
    "What about conditional probability?",
    "Show me a practice problem"
]

for query in conversation:
    response = agent.chat(query)
    print(f"You: {query}")
    print(f"Agent: {response}\n")
```

## Next Steps

1. ✅ Run test script: `python test_rag_chat_agent.py`
2. ✅ Try interactive mode: `python run_rag_chat_agent.py`
3. ✅ Read full documentation: `agents/rag_chat/README.md`
4. ✅ Understand conversion: `agents/rag_chat/CONVERSION_GUIDE.md`
5. ✅ Integrate with orchestrator
6. ✅ Customize prompts and tools as needed

## Support

For issues or questions:
- Check `agents/rag_chat/README.md` for detailed documentation
- Review `agents/rag_chat/CONVERSION_GUIDE.md` for technical details
- Look at `agents/onboarding/` for reference implementation
- Check Strands documentation: https://strandsagents.com/

## Quick Reference

```python
# Basic usage
from agents.rag_chat import RAGChatAgent
agent = RAGChatAgent()
response = agent.chat("Your question here")

# Async usage
response = await agent.chat_async("Your question")

# With custom config
from agents.rag_chat import RAGChatConfig
config = RAGChatConfig()
config.DEFAULT_K = 5
agent = RAGChatAgent(config=config)
```

**You're ready to go! 🚀**
