# Orchestrator Agent - Multi-Agent Architecture

## Overview

The orchestrator coordinates multiple specialized agents using the **agents-as-tools** pattern from Strands. This allows intelligent routing of user requests to the appropriate agents.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                     │
│  (Intelligent request routing & agent coordination)       │
└───────────┬──────────────────────────────────────────────┘
            │
            ├─────────────────────────────────────────────┐
            │                                             │
            ▼                                             ▼
┌───────────────────────┐                    ┌───────────────────────┐
│   ONBOARDING AGENT    │                    │  CONTENT GEN AGENT   │
│  (User assessment)    │                    │  (PDF/Slides maker)  │
└───────────────────────┘                    └───────────────────────┘
            │                                             ▲
            │                                             │
            ▼                                             │
┌───────────────────────┐                                 │
│    USER PROFILE       │                                 │
│  (Memory/Storage)     │─────────────────────────────────┤
└───────────────────────┘                                 │
                                                          │
                                            ┌─────────────┴──────────┐
                                            │     RAG SYSTEM         │
                                            │  (Knowledge retrieval) │
                                            └────────────────────────┘
```

## Components

### 1. Orchestrator Agent (`orchestrator.py`)

The main coordinator that wraps specialized agents as tools:

**Available Tools:**
- `assess_new_user` - Invoke onboarding agent for user assessment
- `retrieve_knowledge` - Query RAG system for relevant content
- `generate_content` - Create PDFs or slides using content agent
- `get_user_profile` - Retrieve stored user information

**Responsibilities:**
- Route requests to appropriate agents
- Maintain user profile memory
- Coordinate multi-step workflows
- Personalize responses based on user level

### 2. Adapter (`adapter.py`)

Translates between orchestrator and content generation agent:

**Functions:**
- `create_content_generation_request()` - Main entry point
  - Formats RAG chunks with structured metadata
  - Creates personalized prompts based on user profile
  - Handles slides vs PDF differentiation

**RAG Chunk Schema:**
```python
{
    'id': str,
    'text': str,
    'topics': List[str],
    'chunk_type': 'definition' | 'example' | 'explanation' | ...,
    'difficulty_level': 'basic' | 'intermediate' | 'advanced',
    'prerequisites': List[str],
    'source_url': str
}
```

**User Profile Schema:**
```python
UserProfile:
    user_id: str
    competence_level: 'easy' | 'medium' | 'difficult'
    ability_score: float
    strengths: List[str]
    weaknesses: List[str]
    recommended_starting_level: str
```

### 3. Specialized Agents

#### Onboarding Agent
- Administers adaptive assessments
- Generates user profiles
- Determines competence levels

#### Content Generation Agent  
- Creates PDF documents
- Generates presentation slides
- Formats markdown content

## Usage Examples

### Basic Setup

```python
from agents.orchestrator.orchestrator import create_orchestrator

# Create orchestrator (optionally with RAG system)
orchestrator = create_orchestrator()

# Simple chat
response = orchestrator.chat("Hello! What can you help me with?")
```

### With User Profile

```python
# Assess new user (returns profile)
user_id = "student_123"
# Profile is automatically stored in orchestrator.user_profiles

# Personalized content generation
response = orchestrator.chat(
    "Create slides on conditional probability",
    user_id=user_id
)
```

### Direct Adapter Usage (for testing)

```python
from agents.orchestrator.adapter import create_content_generation_request

# Mock RAG chunks
chunks = [
    {
        'id': '1',
        'text': 'Definition of conditional probability...',
        'topics': ['conditional probability'],
        'chunk_type': 'definition',
        'difficulty_level': 'basic',
        'prerequisites': ['basic probability'],
        'source_url': 'ncert_ch15'
    }
]

# Generate request
request = create_content_generation_request(
    topic="Conditional Probability",
    request_type="slides",
    rag_chunks=chunks,
    user_profile=my_profile,
    num_slides=10,
    include_exercises=True
)

# Use prompt with content agent
result = content_agent.chat(request['prompt'])
```

## Integration with FastAPI

The orchestrator is designed for easy FastAPI integration:

```python
from fastapi import FastAPI
from agents.orchestrator.orchestrator import create_orchestrator

app = FastAPI()
orchestrator = create_orchestrator()

@app.post("/chat")
async def chat(message: str, user_id: Optional[str] = None):
    response = orchestrator.chat(message, user_id=user_id)
    return {"response": response}

@app.post("/assess")
async def assess(user_id: str):
    # Orchestrator will invoke onboarding agent
    response = orchestrator.chat(
        f"Assess user {user_id}",
        user_id=user_id
    )
    return {"response": response}

@app.post("/generate")
async def generate(
    topic: str, 
    format: str,
    user_id: Optional[str] = None
):
    response = orchestrator.chat(
        f"Generate {format} on {topic}",
        user_id=user_id
    )
    return {"response": response}
```

## Workflow Examples

### 1. New User Onboarding
```
User: "I'm new here"
  ↓
Orchestrator detects new user
  ↓
Invokes assess_new_user tool
  ↓
Onboarding Agent runs assessment
  ↓
Profile stored in orchestrator.user_profiles
  ↓
Returns welcome message with competence level
```

### 2. Content Generation Request
```
User: "Create slides on probability"
  ↓
Orchestrator identifies content request
  ↓
Calls retrieve_knowledge("probability", user_id)
  ↓
RAG returns relevant chunks
  ↓
Adapter formats chunks + profile → prompt
  ↓
Calls generate_content with formatted prompt
  ↓
Content Agent creates slides
  ↓
Returns file path and metadata
```

### 3. Personalized Learning
```
User requests content (with user_id)
  ↓
Orchestrator retrieves user profile
  ↓
RAG query personalized by competence level
  ↓
Adapter adjusts:
  - Language complexity
  - Examples difficulty
  - Number of exercises
  ↓
Content Agent generates personalized material
```

## Testing

Run the complete example:
```bash
cd agents/orchestrator
python complete_example.py
```

Test adapter only (no AWS needed):
```bash
python adapter.py
```

Test orchestrator (requires AWS credentials):
```bash
python orchestrator.py
```

## Configuration

### Environment Variables
- `AWS_PROFILE` - AWS profile for Bedrock access
- `AWS_REGION` - AWS region (default: us-east-1)

### Customization

**Adding New Agents:**
1. Create agent in `agents/<agent_name>/`
2. Add tool wrapper in `orchestrator._create_orchestrator_tools()`
3. Update system prompt with usage guidelines

**Modifying RAG Integration:**
- Implement RAG system with `.query()` method
- Pass to orchestrator: `create_orchestrator()`
- Update `retrieve_knowledge` tool if needed

## Files

- `orchestrator.py` - Main orchestrator implementation
- `adapter.py` - Request formatting and translation layer
- `complete_example.py` - Comprehensive demo examples
- `orchestrator_example.py` - Legacy example (kept for reference)
- `test_adapter.py` - Unit tests for adapter
- `README.md` - This file

## Best Practices

1. **Always retrieve knowledge before generation**
   - Don't generate content without RAG chunks
   - Ensures factual accuracy

2. **Personalize when possible**
   - Check for user_id and profile
   - Adjust difficulty and complexity

3. **Handle errors gracefully**
   - Tools return `{"success": False, "error": "..."}` on failure
   - Orchestrator can retry or suggest alternatives

4. **Log key operations**
   - Use logger for debugging
   - Track tool invocations and results

## Next Steps

- [ ] Add more specialized agents (quiz generator, tutor, etc.)
- [ ] Implement persistent user profile storage (database)
- [ ] Add conversation history/context management
- [ ] Create FastAPI endpoints
- [ ] Add authentication and authorization
- [ ] Implement rate limiting and caching

## Related Documentation

- [Strands Agents as Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agents-as-tools/)
- [Content Generation Agent](../content_generation/README.md)
- [Onboarding Agent](../onboarding/README.md)
- [RAG Schema](../../rag/schema.py)
- [Shared Models](../../shared/models.py)
