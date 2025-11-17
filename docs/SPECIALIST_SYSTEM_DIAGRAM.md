# Specialist Agent System Diagram

## Complete System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                          USER INTERFACE                                │
│                     (Chat Frontend / API)                              │
│                                                                        │
└───────────────────────────────┬────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                          ORCHESTRATOR                                  │
│                    (Workflow Coordination)                             │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                      CLASSIFIER                               │    │
│  │  ┌────────────────────────────────────────────────────────┐  │    │
│  │  │  Query: "Solve: x^2 - 5x + 6 = 0"                      │  │    │
│  │  │                                                          │  │    │
│  │  │  Keywords: ["solve", "equation"]                        │  │    │
│  │  │  → Type: "domain_query"                                 │  │    │
│  │  │  → Agents: ["retriever", "specialist"]                  │  │    │
│  │  │  → Workflow: sequential                                 │  │    │
│  │  └────────────────────────────────────────────────────────┘  │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
└───────────────────────────────┬────────────────────────────────────────┘
                                │
                                ▼
        ┌───────────────────────┴───────────────────────┐
        │                                               │
        ▼                                               ▼
┌───────────────────┐                       ┌───────────────────┐
│                   │                       │                   │
│  RETRIEVAL AGENT  │                       │ SPECIALIST AGENT  │
│     (Step 1)      │                       │    (Step 2)       │
│                   │                       │                   │
└─────────┬─────────┘                       └─────────┬─────────┘
          │                                           │
          │                                           │
          ▼                                           ▼
┌─────────────────────────────┐         ┌─────────────────────────────┐
│                             │         │                             │
│    RAG SYSTEM               │         │  LFM2-350M-Math Model       │
│  (Vector Database)          │         │  (HuggingFace)              │
│                             │         │                             │
│  Query: "quadratic equation"│         │  Input: Problem + Context   │
│                             │         │                             │
│  Retrieved:                 │         │  Process:                   │
│  ┌─────────────────────┐   │         │  1. Tokenize input          │
│  │ Factoring examples  │   │         │  2. Generate solution       │
│  │ Quadratic formula   │───┼─────────┼─►3. Step-by-step work       │
│  │ Similar problems    │   │         │  4. Decode output           │
│  └─────────────────────┘   │         │                             │
│                             │         │  Output:                    │
│                             │         │  "x^2-5x+6 = (x-2)(x-3)=0  │
│                             │         │   Therefore x=2 or x=3"     │
│                             │         │                             │
└─────────────────────────────┘         └─────────────────────────────┘
```

## Component Responsibilities

### 1. Orchestrator
**File:** `agents/orchestrator/orchestrator.py`
- Receives user queries
- Classifies query type
- Routes to appropriate agents
- Manages workflow execution
- Synthesizes final response

### 2. Classifier
**File:** `agents/orchestrator/classifier.py`
- Rule-based + LLM classification
- Identifies query intent
- Determines agent workflow
- Returns confidence scores

### 3. Retrieval Agent
**File:** `agents/retrieval/agent.py`
- Searches knowledge base
- Extracts relevant content
- Provides context for other agents
- Uses semantic + keyword search

### 4. Specialist Agent
**File:** `agents/specialist/agent.py`
- Solves mathematical problems
- Uses finetuned LFM2-350M-Math
- Generates step-by-step solutions
- Leverages RAG context

## Data Flow Example

### User Query: "Solve: x^2 - 5x + 6 = 0"

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Classification                                          │
├─────────────────────────────────────────────────────────────────┤
│ Input: "Solve: x^2 - 5x + 6 = 0"                               │
│ Classifier checks keywords: ["solve", "equation"]              │
│ Result: query_type = "domain_query"                            │
│ Workflow: ["retriever", "specialist"]                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Retrieval                                               │
├─────────────────────────────────────────────────────────────────┤
│ Retriever searches for: "quadratic equation solving"           │
│                                                                 │
│ Returns:                                                        │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ Definition: Quadratic equations have form ax²+bx+c=0    │   │
│ │                                                          │   │
│ │ Example: Factor x²-5x+6 by finding factors of 6 that    │   │
│ │          sum to -5: (x-2)(x-3) = 0                      │   │
│ │                                                          │   │
│ │ Formula: x = [-b ± √(b²-4ac)] / 2a                      │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ Context length: ~500 chars                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Specialist Processing                                   │
├─────────────────────────────────────────────────────────────────┤
│ Input:                                                          │
│   Problem: "Solve: x^2 - 5x + 6 = 0"                           │
│   Context: [Factoring examples and formula]                    │
│                                                                 │
│ LFM2-350M-Math Model:                                           │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ 1. Tokenize: [solve, :, x, ^, 2, -, 5, x, ...]         │   │
│ │    Input tokens: ~150                                    │   │
│ │                                                          │   │
│ │ 2. Generate: Using context about factoring...           │   │
│ │    Temperature: 0.6, Top-p: 0.95                       │   │
│ │                                                          │   │
│ │ 3. Decode output: ~500 tokens                           │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ Output:                                                         │
│ "Looking at the equation x² - 5x + 6 = 0:                      │
│                                                                 │
│  We need to factor this quadratic. We look for two numbers     │
│  that multiply to 6 and add to -5.                             │
│                                                                 │
│  Those numbers are -2 and -3:                                  │
│  • (-2) × (-3) = 6 ✓                                          │
│  • (-2) + (-3) = -5 ✓                                         │
│                                                                 │
│  Therefore: (x - 2)(x - 3) = 0                                 │
│                                                                 │
│  Using the zero product property:                              │
│  x - 2 = 0  OR  x - 3 = 0                                     │
│                                                                 │
│  **Final Answer: x = 2 or x = 3**                             │
│                                                                 │
│  Verification:                                                  │
│  x=2: (2)² - 5(2) + 6 = 4 - 10 + 6 = 0 ✓                    │
│  x=3: (3)² - 5(3) + 6 = 9 - 15 + 6 = 0 ✓"                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Response Synthesis                                      │
├─────────────────────────────────────────────────────────────────┤
│ Orchestrator combines outputs:                                  │
│                                                                 │
│ {                                                               │
│   "query": "Solve: x^2 - 5x + 6 = 0",                         │
│   "query_type": "domain_query",                                │
│   "steps": [                                                    │
│     {                                                           │
│       "agent": "retriever",                                    │
│       "output": "[Context about factoring...]",                │
│       "duration_ms": 150                                       │
│     },                                                          │
│     {                                                           │
│       "agent": "specialist",                                   │
│       "output": "[Complete solution...]",                      │
│       "duration_ms": 2500                                      │
│     }                                                           │
│   ],                                                            │
│   "final_response": "[Solution with steps]",                   │
│   "metadata": {                                                 │
│     "duration_ms": 2650,                                       │
│     "agents_used": ["retriever", "specialist"]                │
│   }                                                             │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Interaction Patterns

### Pattern 1: Sequential (Domain Query)
```
User Query → Classifier → Retriever → Specialist → Response
              (domain)      (context)   (solution)
```

### Pattern 2: Sequential (Concept Explanation)
```
User Query → Classifier → Retriever → Content Gen → Response
              (concept)     (chunks)    (material)
```

### Pattern 3: Direct (Performance Report)
```
User Query → Classifier → Report Agent → Response
              (report)      (analytics)
```

## File Organization

```
lma-major-project-moya-moye/
│
├── agents/
│   │
│   ├── orchestrator/          # Workflow coordination
│   │   ├── classifier.py     # Query classification
│   │   ├── orchestrator.py   # Main orchestrator
│   │   └── adapter.py         # Data transformation
│   │
│   ├── retrieval/             # RAG system
│   │   ├── agent.py          # RAG chat agent
│   │   ├── tools.py          # Search tools
│   │   └── backend/
│   │       ├── rag_system.py
│   │       ├── keyword_extractor.py
│   │       └── vector_db/
│   │
│   ├── specialist/            # 🆕 NEW: Math problem solver
│   │   ├── agent.py          # Specialist agent
│   │   ├── tools.py          # Problem-solving tools
│   │   ├── config.py         # Configuration
│   │   ├── prompts.py        # System prompts
│   │   ├── README.md         # Documentation
│   │   └── QUICKSTART.md     # Quick start
│   │
│   ├── content_generation/    # Content creation
│   │   └── agent.py
│   │
│   └── onboarding/            # User onboarding
│       └── agent.py
│
├── run_specialist_agent.py    # 🆕 Example runner
├── test_specialist_agent.py   # 🆕 Test suite
│
└── Documentation/             # 🆕 Implementation docs
    ├── SPECIALIST_AGENT_COMPLETE.md
    ├── SPECIALIST_ORCHESTRATOR_INTEGRATION.md
    └── SPECIALIST_AGENT_DONE.md
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                      │
├─────────────────────────────────────────────────────────┤
│  • Strands Agent Framework (Coordination)               │
│  • Python 3.8+ (Runtime)                                │
│  • DSPy (LLM interactions)                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    AGENT LAYER                          │
├─────────────────────────────────────────────────────────┤
│  • RAG Chat Agent (Retrieval)                           │
│  • Specialist Agent (Problem Solving)                   │
│  • Content Generator (Material Creation)                │
│  • Onboarding Agent (User Profiling)                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    MODEL LAYER                          │
├─────────────────────────────────────────────────────────┤
│  • LFM2-350M-Math (Specialist reasoning)                │
│  • Claude Sonnet 4 (Classification, RAG)                │
│  • HuggingFace Transformers (Model loading)             │
│  • SpaCy NER (Keyword extraction)                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                           │
├─────────────────────────────────────────────────────────┤
│  • ChromaDB (Vector database)                           │
│  • SQLite (User profiles, metadata)                     │
│  • JSON (Configuration, chunks)                         │
└─────────────────────────────────────────────────────────┘
```

## Performance Characteristics

```
Operation                    Cold Start    Warm Start    Notes
─────────────────────────────────────────────────────────────────
Orchestrator Init            ~100ms        ~50ms        Light
Retriever Init               ~200ms        ~100ms       Load vector DB
Specialist Init (First)      10-30s        <1s          Download model
Specialist Init (Cached)     ~1s           <100ms       Model in memory

Query Processing:
  Classification             ~50ms         ~50ms        Rule + LLM
  Retrieval                  ~150ms        ~100ms       Semantic search
  Specialist Inference:
    - GPU                    1-3s          1-3s         CUDA acceleration
    - CPU                    5-15s         5-15s        Slower but works
  
Total (domain_query):
  - First time              15-35s         N/A          Model download
  - Subsequent (GPU)        2-4s           2-4s         Optimal
  - Subsequent (CPU)        6-16s          6-16s        Acceptable
```

## Memory Footprint

```
Component                Memory Usage      Disk Space
──────────────────────────────────────────────────────
Orchestrator            ~50MB              ~1MB
Retrieval Agent         ~150MB             ~100MB (DB)
Specialist Agent:
  - Model on disk       N/A                ~1.4GB
  - Loaded (GPU)        ~2-3GB GPU         -
  - Loaded (CPU)        ~4-6GB RAM         -

Total System:
  - Minimal             ~200MB RAM         ~100MB
  - With Specialist     ~2-3GB GPU         ~1.5GB
                        or
                        ~4-6GB RAM
```

---

**🎉 The Specialist Math Agent is fully integrated and ready to solve problems!**
