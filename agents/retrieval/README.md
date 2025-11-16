# RAG Chat Agent

A Strands-based intelligent tutoring agent that uses Retrieval-Augmented Generation (RAG) to provide high-quality educational content about probability and statistics.

## Overview

The RAG Chat Agent combines several technologies to create an effective educational tutor:

- **Retrieval System**: Uses ChromaDB for semantic search over educational content
- **Keyword Extraction**: Custom NER model + fuzzy matching for topic identification
- **Metadata Filtering**: Precise content filtering by type, difficulty, and topics
- **LLM Teaching**: Claude Sonnet 4 on AWS Bedrock for explanations and tutoring
- **Strands Framework**: Orchestrates tools and conversation flow

## Architecture

```
RAGChatAgent
├── Agent (Strands)
│   ├── Model: AWS Bedrock (Claude Sonnet 4)
│   ├── System Prompt: Teaching instructions
│   └── Tools: [search_knowledge_base, get_related_topics, get_prerequisites, get_stats]
│
├── Tools Backend
│   ├── RAGSystem: Vector search + metadata filtering
│   ├── KeywordExtractor: NER + fuzzy matching
│   └── MetadataExtractor: DSPy-based chunk type determination
│
└── Knowledge Base (ChromaDB)
    └── Educational chunks with rich metadata
```

## Features

### Content Types

The agent can retrieve 9 different types of educational content:

1. **Definitions**: Formal definitions of concepts
2. **Examples**: Concrete examples demonstrating concepts
3. **Explanations**: Detailed explanations of topics
4. **Proofs**: Mathematical proofs of theorems
5. **Visualizations**: Visual representations of concepts
6. **Practice Problems**: Problems for students to solve
7. **Worked Solutions**: Step-by-step solutions
8. **Analogies**: Relatable analogies for abstract concepts
9. **Misconceptions**: Common mistakes and how to avoid them

### Adaptive Retrieval

- Automatically extracts keywords from student questions
- Determines the most appropriate content type using LLM
- Filters by difficulty level (basic, intermediate, advanced)
- Falls back gracefully when specific content isn't available

### Teaching Capabilities

- Combines multiple content types for comprehensive learning
- Checks prerequisites when students struggle
- Provides related topics for broader context
- Uses pedagogically sound teaching principles

## Tools

### 1. `search_knowledge_base`

The primary tool for retrieving educational content.

**Parameters:**
- `query` (str): Student's question or topic
- `chunk_type` (optional): Type of content to retrieve
- `topics` (optional): Specific topics to filter by
- `difficulty_level` (optional): "basic", "intermediate", or "advanced"
- `k` (int): Number of pieces to retrieve (default: 3)

**Examples:**
```python
# Get a definition
search_knowledge_base("What is conditional probability?", chunk_type="definition")

# Get examples about specific topics
search_knowledge_base("probability distributions", chunk_type="example", topics=["probability"])

# Let the system determine the best content type
search_knowledge_base("I don't understand Bayes theorem")
```

### 2. `get_related_topics`

Find concepts related to a given topic for broader context.

**Parameters:**
- `topic` (str): The main topic
- `k` (int): Number of related topics (default: 5)

### 3. `get_prerequisites`

Identify prerequisite concepts that students should learn first.

**Parameters:**
- `topic` (str): The topic to find prerequisites for

### 4. `get_knowledge_base_stats`

Get statistics about the available content in the knowledge base.

## Configuration

Environment variables (optional):

```bash
# AWS Configuration
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0

# RAG Configuration
RAG_DB_PATH=./rag/prob_db
RAG_MODEL_NAME=all-MiniLM-L6-v2
RAG_DEFAULT_K=3

# Keyword Extraction
KEYWORDS_FILE=keyword_extractor/probability_keywords.csv
NER_MODEL_PATH=keyword_extractor/math_ner_model

# Logging
AGENT_VERBOSE=true
```

## Usage

### Basic Usage

```python
from agents.rag_chat import RAGChatAgent

# Create agent
agent = RAGChatAgent()

# Welcome message
print(agent.welcome())

# Chat with the agent
response = agent.chat("What is conditional probability?")
print(response)

# Continue conversation
response = agent.chat("Can you show me an example?")
print(response)
```

### Async Usage

```python
import asyncio
from agents.rag_chat import RAGChatAgent

async def main():
    agent = RAGChatAgent()
    response = await agent.chat_async("Explain Bayes theorem")
    print(response)

asyncio.run(main())
```

### Custom Configuration

```python
from agents.rag_chat import RAGChatAgent, RAGChatConfig

# Create custom config
config = RAGChatConfig()
config.DEFAULT_K = 5
config.RAG_DB_PATH = "./custom_db"

# Create agent with custom config
agent = RAGChatAgent(config=config)
```

## Running the Agent

### Interactive Mode

```bash
# Run the example script
python run_rag_chat_agent.py
```

### As a Module

```python
from agents.rag_chat import create_rag_chat_agent

agent = create_rag_chat_agent()

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    
    response = agent.chat(user_input)
    print(f"Agent: {response}")
```

## Integration with Orchestrator

The RAG Chat Agent is designed to be used as a specialized agent within the larger orchestrator system:

```python
from agents.orchestrator import Orchestrator
from agents.rag_chat import RAGChatAgent

# Create orchestrator
orchestrator = Orchestrator()

# Add RAG chat agent as a specialized tutor
rag_agent = RAGChatAgent()
orchestrator.add_agent("tutor", rag_agent)

# Route tutoring questions to RAG agent
response = orchestrator.route_query(
    "Explain conditional probability",
    preferred_agent="tutor"
)
```

## Example Interactions

### Example 1: Learning a Definition

**Student:** "What is conditional probability?"

**Agent:**
1. Calls `search_knowledge_base(query="What is conditional probability?", chunk_type="definition")`
2. Presents the formal definition clearly
3. Calls `search_knowledge_base(chunk_type="example")` to get a concrete example
4. Explains the example in simple terms
5. Asks if the student wants to see practice problems

### Example 2: Struggling with a Concept

**Student:** "I don't understand Bayes' theorem"

**Agent:**
1. Calls `get_prerequisites(topic="Bayes theorem")` to check what they should know first
2. Calls `search_knowledge_base(query="Bayes theorem", chunk_type="explanation")`
3. Presents a clear, step-by-step explanation
4. Calls `search_knowledge_base(chunk_type="analogy")` for a relatable analogy
5. Calls `search_knowledge_base(chunk_type="worked_solution")` to show a concrete example
6. Checks understanding and offers more practice

### Example 3: Practice Problems

**Student:** "Can you give me a probability problem to solve?"

**Agent:**
1. Calls `search_knowledge_base(chunk_type="practice_problem")`
2. Presents the problem clearly
3. Waits for student's attempt or request for help
4. When asked, calls `search_knowledge_base(chunk_type="worked_solution")`
5. Provides step-by-step guidance and feedback

## Benefits Over Original Implementation

1. **Structured Tool Use**: Strands framework provides better tool orchestration
2. **Conversation Memory**: Agent maintains context across turns
3. **Error Handling**: Graceful fallbacks when content isn't found
4. **Extensibility**: Easy to add new tools and capabilities
5. **Integration**: Works seamlessly with other agents in the system
6. **Observability**: Built-in logging and monitoring through Strands
7. **Async Support**: Native async/await for better performance

## Dependencies

- `strands`: Agent framework
- `chromadb`: Vector database
- `dspy`: Metadata extraction
- `sentence-transformers`: Text embeddings
- `spacy`: NER for keyword extraction
- `rapidfuzz`: Fuzzy string matching
- `boto3`: AWS Bedrock access

## Development

### Running Tests

```bash
pytest tests/agents/test_rag_chat.py
```

### Adding New Tools

1. Define the tool function in `tools.py` with the `@tool` decorator
2. Add comprehensive docstring with examples
3. Add the tool to the `rag_chat_tools` list
4. Update `AGENT_INSTRUCTIONS` in `prompts.py` to explain the new tool

### Customizing Teaching Behavior

Edit the `AGENT_INSTRUCTIONS` in `prompts.py` to modify:
- Teaching style and tone
- Content selection strategy
- Follow-up questions
- Error handling approach

## Troubleshooting

### No content found errors
- Check that the knowledge base is populated: `RAGSystem(db_path).get_stats()`
- Verify keyword extraction is working: `KeywordExtractor().extract_keywords(query)`
- Try broader search terms or remove filters

### Slow responses
- Reduce the number of retrieval calls (`k` parameter)
- Use more specific queries to reduce LLM processing time
- Enable async mode for concurrent operations

### AWS Bedrock errors
- Verify AWS credentials are configured
- Check that the model ID is correct for your region
- Ensure you have quota for the selected model

## License

Part of the LMA Major Project.
