# Workflow-Based Orchestrator

## Overview

The `WorkflowOrchestrator` is a production-ready orchestration system that coordinates multiple specialized agents using a classifier-based workflow routing approach.

## Architecture

```
User Query
    ↓
Classifier (Rule-based + LLM)
    ↓
Workflow Selection
    ↓
Sequential Agent Execution
    ↓
Response Synthesis
    ↓
Final Response
```

## Key Features

### 1. **Intelligent Classification**
- Hybrid approach: Rule-based + optional LLM classification
- Multiple query types supported:
  - `concept_explanation` - Educational content
  - `assessment` - Quizzes and tests
  - `performance_report` - Analytics and progress
  - `domain_query` - Problem solving
  - `content_creation` - Slides, PDFs, etc.

### 2. **Workflow-Based Routing**
Each query type has a predefined workflow:

```python
"concept_explanation": {
    "agents": ["retriever", "content_generation"],
    "workflow": "sequential"
}
```

### 3. **Structured Logging**
- Comprehensive traces for debugging
- Performance metrics (timing, agent usage)
- Structured JSON logging compatible with log aggregation tools

### 4. **User Profile Management**
- Store and retrieve user profiles
- Personalize responses based on competence level
- Context-aware agent routing

## Usage

### Basic Usage

```python
from agents.orchestrator.workflow_orchestrator import create_workflow_orchestrator
from agents.retrieval.backend.rag_system import RAGSystem

# Initialize with RAG system
rag = RAGSystem()
orchestrator = create_workflow_orchestrator(rag_system=rag)

# Process a query
result = orchestrator.process_query(
    query="Explain probability theory",
    user_id="user123"
)

print(result["final_response"])
```

### Advanced Usage

```python
# Store user profile
from shared.models import UserProfile

profile = UserProfile(
    user_id="user123",
    competence_level="intermediate",
    ability_score=0.5
)
orchestrator.store_profile("user123", profile)

# Process with full context
result = orchestrator.process_query(
    query="Create slides on linear algebra",
    user_id="user123",
    context="Previous topic: Vector spaces"
)

# Access detailed execution trace
print(f"Query Type: {result['query_type']}")
print(f"Agents Used: {result['metadata']['agents_used']}")
print(f"Duration: {result['metadata']['duration_ms']}ms")

for step in result['steps']:
    print(f"Agent: {step['agent']}, Success: {step['success']}")
```

## Integration with FastAPI

Update your `api_server/main.py`:

```python
from agents.orchestrator.workflow_orchestrator import create_workflow_orchestrator

# In lifespan function
orchestrator_agent = create_workflow_orchestrator(rag_system=rag_system)

# In handle_orchestrator function
async def handle_orchestrator(user_id: str, message: str, session: dict):
    profile = session_manager.get_profile(user_id)
    
    if not profile:
        return (
            "Please complete onboarding first.",
            {"agent": "Orchestrator", "needs_onboarding": True}
        )
    
    # Store profile in orchestrator
    orchestrator_agent.store_profile(user_id, profile)
    
    # Process query
    result = orchestrator_agent.process_query(
        query=message,
        user_id=user_id
    )
    
    return result["final_response"], {
        "agent": "Orchestrator",
        "query_type": result["query_type"],
        "agents_used": result["metadata"]["agents_used"],
        "duration_ms": result["metadata"]["duration_ms"]
    }
```

## Agent Communication Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Client (Frontend)                     │
└─────────────┬──────────────────────────────┬────────────┘
              │                              │
              │ WebSocket/REST               │
              │                              │
┌─────────────▼──────────────┐   ┌──────────▼─────────────┐
│   Onboarding Agent         │   │  Workflow Orchestrator │
│   (Direct Connection)      │   │                        │
└────────────────────────────┘   └──────────┬─────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
        ┌───────────▼──────────┐ ┌──────────▼────────┐  ┌───────────▼─────────┐
        │  Retriever Agent     │ │ Content Gen Agent │  │   Quiz Agent        │
        │  (Context Provider)  │ │                   │  │                     │
        └──────────────────────┘ └───────────────────┘  └─────────────────────┘
                                             │
                                 ┌───────────▼──────────┐
                                 │   Report Agent       │
                                 │                      │
                                 └──────────────────────┘
```

## Workflow Examples

### 1. Concept Explanation
```
Query: "Explain how neural networks work"
  ↓
Classifier: concept_explanation
  ↓
Workflow: ["retriever", "content_generation"]
  ↓
Retriever: Fetch relevant educational content
  ↓
Content Gen: Generate structured explanation
  ↓
Synthesis: Combine context + explanation
  ↓
Response: Comprehensive explanation with references
```

### 2. Assessment
```
Query: "Give me a quiz on statistics"
  ↓
Classifier: assessment
  ↓
Workflow: ["retriever", "quiz"]
  ↓
Retriever: Fetch statistics content
  ↓
Quiz Agent: Generate personalized quiz
  ↓
Response: Interactive quiz questions
```

### 3. Content Creation
```
Query: "Create slides about machine learning"
  ↓
Classifier: content_creation
  ↓
Workflow: ["retriever", "content_generation"]
  ↓
Retriever: Fetch ML topics and examples
  ↓
Content Gen: Generate presentation slides
  ↓
Response: Link to generated PDF/slides
```

## Adding New Agents

To add a new agent:

1. **Implement the agent:**
```python
class MyNewAgent:
    def process(self, query: str, context: str, user_profile: UserProfile):
        # Agent logic here
        return "Agent response"
```

2. **Register in orchestrator:**
```python
# In __init__
self.my_agent = MyNewAgent()
self.agents["my_agent"] = self.my_agent
```

3. **Add to classifier workflow:**
```python
# In classifier.py
"my_query_type": {
    "description": "My new query type",
    "keywords": ["keyword1", "keyword2"],
    "agents": ["retriever", "my_agent"],
    "workflow": "sequential"
}
```

4. **Implement call method:**
```python
def _call_my_agent(self, query: str, retrieved: str, user_profile: Optional[UserProfile]) -> str:
    return self.my_agent.process(query, retrieved, user_profile)
```

## Performance Considerations

- **Average latency**: 500-2000ms depending on agents used
- **Retriever**: ~200-500ms
- **Content Generation**: ~1000-3000ms
- **Classification**: ~50-200ms (rule-based), ~500ms (LLM)

## Logging & Monitoring

All operations are logged with structured JSON:

```json
{
  "timestamp_ms": 1699999999999,
  "duration_ms": 1250,
  "user_id": "user123",
  "query": "Explain probability",
  "query_type": "concept_explanation",
  "classification_scores": {"concept_explanation": 2, "assessment": 0},
  "steps": [
    {
      "agent": "retriever",
      "duration_ms": 350,
      "success": true,
      "output_summary": "Retrieved 5 chunks..."
    },
    {
      "agent": "content_generation",
      "duration_ms": 900,
      "success": true,
      "output_summary": "Generated explanation..."
    }
  ]
}
```

## Testing

Run the test suite:

```bash
cd agents/orchestrator
python workflow_orchestrator.py
```

## Comparison: Workflow vs Agents-as-Tools

| Feature | Workflow Orchestrator | Agents-as-Tools |
|---------|----------------------|-----------------|
| **Predictability** | High - predefined flows | Lower - LLM decides |
| **Latency** | Lower (~500-2000ms) | Higher (~1000-4000ms) |
| **Control** | Explicit workflows | Implicit via prompts |
| **Debugging** | Easy to trace | Harder to debug |
| **Flexibility** | Requires code changes | More adaptable |
| **Reliability** | Very reliable | Depends on LLM |

## Recommendation

✅ **Use Workflow Orchestrator for:**
- Production systems requiring reliability
- Cost-sensitive applications
- Latency-critical use cases
- Systems with well-defined query types

⚠️ **Use Agents-as-Tools for:**
- Exploratory/research systems
- Highly dynamic query types
- Systems where flexibility > predictability
- Prototyping and experimentation

## Future Enhancements

- [ ] Parallel agent execution where possible
- [ ] Agent result caching
- [ ] Dynamic workflow adjustment based on results
- [ ] Agent health monitoring
- [ ] Fallback strategies for agent failures
- [ ] A/B testing between different workflows
- [ ] Real-time workflow visualization
