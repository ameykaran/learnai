# Multi-Agent System Architecture

## System Overview

Your adaptive learning system uses a **workflow-based orchestration pattern** where a central orchestrator coordinates multiple specialized agents based on query classification.

```
┌────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│  (React Frontend + WebSocket/REST Communication)                    │
└────────────┬───────────────────────────────────────┬───────────────┘
             │                                       │
             │ Direct Connection                     │ Via Orchestrator
             │                                       │
┌────────────▼────────────┐            ┌────────────▼─────────────────┐
│                         │            │                              │
│   ONBOARDING AGENT      │            │   WORKFLOW ORCHESTRATOR      │
│   (Direct to Client)    │            │   (Central Coordinator)      │
│                         │            │                              │
│  • Adaptive Testing     │            │  • Query Classification      │
│  • Profile Creation     │            │  • Workflow Routing          │
│  • Competence Assessment│            │  • Agent Coordination        │
│                         │            │  • Response Synthesis        │
└─────────────────────────┘            └──────────┬───────────────────┘
                                                   │
                    ┌──────────────────────────────┼───────────────────────────┐
                    │                              │                           │
        ┌───────────▼──────────┐     ┌────────────▼───────────┐   ┌──────────▼─────────┐
        │                      │     │                        │   │                    │
        │  RETRIEVER AGENT     │     │  CONTENT GEN AGENT     │   │   QUIZ AGENT       │
        │  (Knowledge Provider)│     │  (Content Creator)     │   │   (Assessment Gen) │
        │                      │     │                        │   │                    │
        │  • RAG System        │     │  • PDF Generation      │   │  • Dynamic Quizzes │
        │  • Vector Search     │     │  • Slide Creation      │   │  • Adaptive Tests  │
        │  • Context Retrieval │     │  • Markdown Rendering  │   │  • Level-based     │
        └──────────────────────┘     └────────────────────────┘   └────────────────────┘
                                                   │
                                       ┌───────────▼───────────┐
                                       │                       │
                                       │   REPORT AGENT        │
                                       │   (Analytics)         │
                                       │                       │
                                       │  • Performance Data   │
                                       │  • Progress Tracking  │
                                       │  • Email/PDF Reports  │
                                       └───────────────────────┘
```

## Query Flow Architecture

### Complete Request Flow

```
1. CLIENT
   │
   │ HTTP POST/WebSocket
   ├─→ "Explain probability theory"
   │
2. API SERVER (main.py)
   │
   │ Route to handler
   ├─→ handle_orchestrator() or handle_onboarding()
   │
3. SESSION MANAGER
   │
   │ Check user profile
   ├─→ Profile exists? → Continue
   └─→ No profile? → Redirect to onboarding
   │
4. WORKFLOW ORCHESTRATOR
   │
   │ Step 1: Classification
   ├─→ Classifier.classify()
   │   ├─→ Rule-based matching
   │   └─→ Optional LLM classification
   │   Result: "concept_explanation"
   │
   │ Step 2: Workflow Selection
   ├─→ Get workflow for query type
   │   Workflow: ["retriever", "content_generation"]
   │
   │ Step 3: Sequential Agent Execution
   ├─→ Execute Retriever Agent
   │   │ Query: "probability theory"
   │   │ User Profile: intermediate level
   │   └─→ Returns: 5 relevant chunks
   │
   ├─→ Execute Content Generation Agent
   │   │ Input: Query + Retrieved chunks
   │   └─→ Returns: Structured explanation
   │
   │ Step 4: Response Synthesis
   ├─→ Combine agent outputs
   │   └─→ Final response with references
   │
5. API SERVER
   │
   │ Add metadata
   ├─→ Return to client with timing, agent info
   │
6. CLIENT
   │
   └─→ Display response to user
```

## Agent Communication Patterns

### Pattern 1: Direct Connection (Onboarding)

```
Client ←──────────→ Onboarding Agent
       Direct WS/REST
       
• Used for: Initial user assessment
• Reason: Requires multi-turn conversation
• Profile Storage: Saved to orchestrator's memory after completion
```

### Pattern 2: Orchestrator-Mediated (All Other Agents)

```
Client ←→ Orchestrator ←→ [Retriever, Content Gen, Quiz, Report]
                
• Used for: All post-onboarding interactions
• Reason: Enables intelligent routing and context sharing
• Response Flow: Client → Orch → Agent(s) → Orch → Client
```

### Pattern 3: Sequential Pipeline

```
Query → Retriever → Content Gen → Response
        (Context)   (Generation)
        
• Retriever always runs first (if needed)
• Provides context to downstream agents
• Used by: concept_explanation, content_creation, assessment
```

## Workflow Definitions

### 1. Concept Explanation
```yaml
Query: "Explain [topic]"
Classification: concept_explanation
Agents: [retriever, content_generation]
Flow:
  1. Retriever fetches relevant educational content
  2. Content Gen creates structured explanation
  3. Synthesis combines context + explanation
Response: Comprehensive educational content
```

### 2. Assessment/Quiz
```yaml
Query: "Give me a quiz on [topic]"
Classification: assessment
Agents: [retriever, quiz]
Flow:
  1. Retriever fetches topic content
  2. Quiz agent generates questions at user's level
  3. Returns interactive quiz
Response: Quiz questions with difficulty matching user profile
```

### 3. Content Creation
```yaml
Query: "Create slides about [topic]"
Classification: content_creation
Agents: [retriever, content_generation]
Flow:
  1. Retriever gathers comprehensive content
  2. Content Gen creates PDF/slides
  3. File saved to public directory
Response: Download link + metadata
```

### 4. Performance Report
```yaml
Query: "Show my progress"
Classification: performance_report
Agents: [report]
Flow:
  1. Report agent accesses user history
  2. Generates analytics and visualizations
  3. Creates PDF/email report
Response: Performance summary + recommendations
Requirement: User must have completed at least one test
```

### 5. Domain Query (Problem Solving)
```yaml
Query: "Solve this equation: ..."
Classification: domain_query
Agents: [retriever, specialist]
Flow:
  1. Retriever finds similar problems/methods
  2. Specialist agent solves the problem
  3. Returns step-by-step solution
Response: Detailed solution with explanations
```

## Data Flow

### User Profile Journey

```
New User
   │
   └─→ Onboarding Agent
       │ Adaptive assessment (10 questions)
       │ Computes competence level
       │ Identifies strengths/weaknesses
       └─→ UserProfile object created
           │
           ├─→ Stored in SessionManager
           ├─→ Loaded into Orchestrator memory
           └─→ Used for personalization in all future queries
```

### Context Passing Between Agents

```
User Query: "Explain neural networks"
   │
   └─→ Orchestrator
       │
       ├─→ Retriever Agent
       │   Input:
       │   • query: "neural networks"
       │   • user_profile: {level: "intermediate", ...}
       │   Output:
       │   • chunks: [{text: "...", difficulty: "medium"}, ...]
       │
       └─→ Content Generation Agent
           Input:
           • query: "Explain neural networks"
           • retrieved_context: [chunks from retriever]
           • user_profile: {level: "intermediate", ...}
           Output:
           • markdown_content: "# Neural Networks\n\n..."
           
Final Response: Synthesized explanation with references
```

## Key Design Decisions

### Why Workflow-Based vs Agents-as-Tools?

| Aspect | Workflow (Chosen) | Agents-as-Tools |
|--------|------------------|-----------------|
| **Control** | Explicit, predictable | LLM-driven, flexible |
| **Latency** | 500-2000ms | 1000-4000ms |
| **Cost** | Lower (fewer LLM calls) | Higher (LLM decides) |
| **Reliability** | High | Moderate |
| **Debugging** | Easy (clear traces) | Harder |
| **Best For** | Production systems | Research/exploration |

**Decision**: Workflow-based for production reliability and cost-efficiency.

### Why Direct Connection for Onboarding?

1. **Multi-turn conversation**: Onboarding requires 10+ back-and-forth interactions
2. **Stateful process**: Must maintain quiz state across messages
3. **Synchronous completion**: Need to wait for full profile before other operations
4. **Isolation**: Onboarding logic is independent of other agents

### Why Sequential Execution?

1. **Dependency chain**: Later agents need context from earlier ones
2. **Simplicity**: Easier to debug and maintain
3. **Resource efficiency**: Avoid unnecessary agent calls
4. **Consistent quality**: Each agent has full context from previous steps

**Future Enhancement**: Parallel execution where agents don't depend on each other (e.g., quiz generation + report generation).

## Integration Points

### 1. API Server (main.py)

```python
# Lifespan: Initialize orchestrator
orchestrator = create_workflow_orchestrator()

# Chat endpoint: Route to appropriate handler
if mode == "onboarding":
    response = await handle_onboarding(...)
else:
    response = await handle_orchestrator(...)
```

### 2. Session Manager

```python
# Store user profiles
session_manager.store_profile(user_id, profile)

# Retrieve for personalization
profile = session_manager.get_profile(user_id)
```

### 3. Orchestrator

```python
# Process query
result = orchestrator.process_query(
    query=message,
    user_id=user_id,
    context=conversation_history
)

# Returns structured result with metadata
{
    "query_type": "concept_explanation",
    "agents_used": ["retriever", "content_generation"],
    "final_response": "...",
    "metadata": {...}
}
```

## Scaling Considerations

### Current Architecture (Monolithic)
```
API Server
  ├─→ Orchestrator (in-process)
  ├─→ All Agents (in-process)
  └─→ RAG System (in-process)
```

### Future Architecture (Microservices)
```
API Gateway
  ├─→ Orchestrator Service
  │   ├─→ Retriever Service (gRPC)
  │   ├─→ Content Gen Service (gRPC)
  │   ├─→ Quiz Service (gRPC)
  │   └─→ Report Service (gRPC)
  └─→ Onboarding Service (Direct)
```

### Migration Path

1. **Phase 1** (Current): Monolithic, in-process agents
2. **Phase 2**: Extract agents to separate modules with interface contracts
3. **Phase 3**: Wrap agents as microservices behind gRPC/REST APIs
4. **Phase 4**: Add service mesh for observability and resilience

## Monitoring & Observability

### Structured Logging

Every query generates a trace:

```json
{
  "timestamp_ms": 1699999999999,
  "user_id": "user123",
  "query": "Explain probability",
  "query_type": "concept_explanation",
  "classification_scores": {"concept_explanation": 2},
  "steps": [
    {"agent": "retriever", "duration_ms": 350, "success": true},
    {"agent": "content_generation", "duration_ms": 900, "success": true}
  ],
  "duration_ms": 1250,
  "final_response_length": 1543
}
```

### Metrics to Track

- **Latency**: Per-agent and end-to-end
- **Success Rate**: Agent execution success percentage
- **Query Distribution**: Which query types are most common
- **Agent Usage**: Which agents are called most frequently
- **User Profiles**: Competence level distribution
- **Error Rates**: Classification errors, agent failures

## Error Handling Strategy

### Agent Failure Handling

```python
try:
    result = agent.process(...)
except Exception as e:
    log.error(f"Agent {name} failed: {e}")
    steps.append({"agent": name, "error": str(e), "success": False})
    # Continue to next agent or synthesize partial response
```

### Fallback Strategies

1. **Retriever Fails**: Use generic knowledge or prompt user for clarification
2. **Content Gen Fails**: Return raw retrieved content
3. **Quiz Fails**: Offer alternative learning resources
4. **Report Fails**: Return summary statistics only

## Security Considerations

1. **User Isolation**: Each user's profile is isolated in session manager
2. **Input Validation**: All queries sanitized before processing
3. **Rate Limiting**: Prevent abuse of expensive operations (content generation)
4. **File Access**: Generated files scoped to user sessions
5. **Profile Privacy**: Profiles stored in-memory only (consider encryption for persistence)

## Next Steps for Enhancement

1. ✅ **Workflow Orchestrator**: Implemented
2. ⏳ **Implement Remaining Agents**: Quiz, Report, Specialist
3. ⏳ **Add Parallel Execution**: For independent agents
4. ⏳ **Caching Layer**: Cache retrieval results
5. ⏳ **A/B Testing**: Test different workflows
6. ⏳ **Real-time Monitoring**: Dashboard for system metrics
7. ⏳ **User Feedback Loop**: Improve agent responses based on user reactions
