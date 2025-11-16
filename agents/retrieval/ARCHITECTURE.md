# RAG Chat Agent Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              User Interface                             │
│                                                                         │
│  • run_rag_chat_agent.py (Interactive CLI)                            │
│  • Web Interface (FastAPI integration)                                │
│  • Orchestrator (Multi-agent system)                                  │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          RAGChatAgent (agent.py)                        │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │              Strands Agent Framework                              │ │
│  │                                                                   │ │
│  │  • Agent Name: RAGChatAssistant                                  │ │
│  │  • Model: Claude Sonnet 4 (AWS Bedrock)                         │ │
│  │  • System Prompt: Teaching instructions                         │ │
│  │  • Tools: 4 registered tools                                    │ │
│  │  • Memory: Conversation context                                 │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Methods:                                                              │
│  • chat(message) → str                                                │
│  • chat_async(message) → str                                          │
│  • welcome() → str                                                    │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Strands Tools (tools.py)                        │
│                                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐                   │
│  │ search_knowledge_base│  │  get_related_topics  │                   │
│  │                      │  │                      │                   │
│  │ • Primary retrieval  │  │ • Find related       │                   │
│  │ • Auto keyword       │  │   concepts           │                   │
│  │   extraction         │  │ • Broader context    │                   │
│  │ • Auto chunk type    │  │                      │                   │
│  │ • Flexible filters   │  │                      │                   │
│  └──────────────────────┘  └──────────────────────┘                   │
│                                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐                   │
│  │  get_prerequisites   │  │ get_kb_stats         │                   │
│  │                      │  │                      │                   │
│  │ • Identify           │  │ • Database info      │                   │
│  │   foundations        │  │ • Content coverage   │                   │
│  │ • Help struggling    │  │                      │                   │
│  │   students           │  │                      │                   │
│  └──────────────────────┘  └──────────────────────┘                   │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     RAGChatTools Backend (tools.py)                     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    Backend Components (Singleton)                │  │
│  │                                                                  │  │
│  │  1. RAGSystem (rag_system.py)                                   │  │
│  │     • ChromaDB integration                                      │  │
│  │     • Vector search (cosine similarity)                         │  │
│  │     • Metadata filtering                                        │  │
│  │     • Progressive relaxation                                    │  │
│  │                                                                  │  │
│  │  2. KeywordExtractor (keyword_extractor.py)                     │  │
│  │     • Custom spaCy NER model                                    │  │
│  │     • Fuzzy matching (RapidFuzz)                                │  │
│  │     • Topic identification                                      │  │
│  │                                                                  │  │
│  │  3. MetadataExtractor (DSPy)                                    │  │
│  │     • Gemini 2.0 Flash                                          │  │
│  │     • Chunk type determination                                  │  │
│  │     • Query classification                                      │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Knowledge Base (ChromaDB)                          │
│                                                                         │
│  Database: ./rag/prob_db/                                              │
│  Collection: educational_chunks                                        │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                     Educational Chunks                            │ │
│  │                                                                   │ │
│  │  Each chunk contains:                                            │ │
│  │  • id: Unique identifier                                         │ │
│  │  • text: Educational content                                     │ │
│  │  • embedding: Vector (384 dimensions)                            │ │
│  │  • metadata:                                                     │ │
│  │    - source_url                                                  │ │
│  │    - source_type                                                 │ │
│  │    - chunk_type (9 types)                                        │ │
│  │    - difficulty_level (3 levels)                                 │ │
│  │    - topics (list)                                               │ │
│  │    - prerequisites (list)                                        │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘


## Data Flow Diagram

┌──────────┐
│   User   │
└────┬─────┘
     │ "What is conditional probability?"
     ▼
┌────────────────┐
│  RAGChatAgent  │
└────┬───────────┘
     │ Passes to Strands Agent
     ▼
┌─────────────────────┐
│  Claude Sonnet 4    │
│  (AWS Bedrock)      │
│                     │
│  Decides to use:    │
│  search_knowledge_  │
│  base()             │
└────┬────────────────┘
     │ Tool call with parameters
     ▼
┌─────────────────────────────┐
│  search_knowledge_base      │
│  @tool                      │
│                             │
│  1. Extract keywords        │
│     • "conditional"         │
│     • "probability"         │
│                             │
│  2. Determine chunk type    │
│     → "definition"          │
│                             │
│  3. Build filters           │
│     • topics: [...]         │
│     • chunk_type:           │
│       "definition"          │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  RAGSystem                  │
│  (rag_system.py)            │
│                             │
│  1. Create query embedding  │
│  2. Apply metadata filters  │
│  3. Query ChromaDB          │
│  4. Return top k chunks     │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  ChromaDB                   │
│  • Vector similarity search │
│  • Filter by metadata       │
│  • Return ranked results    │
└────┬────────────────────────┘
     │ Retrieved chunks
     ▼
┌─────────────────────────────┐
│  search_knowledge_base      │
│  • Format results           │
│  • Return to agent          │
└────┬────────────────────────┘
     │ Formatted content
     ▼
┌─────────────────────────────┐
│  Claude Sonnet 4            │
│  • Analyzes content         │
│  • Crafts teaching response │
│  • May call more tools      │
└────┬────────────────────────┘
     │ Final response
     ▼
┌─────────────────────────────┐
│  RAGChatAgent               │
│  • Returns response to user │
└────┬────────────────────────┘
     │
     ▼
┌──────────┐
│   User   │ "Oh, I understand now!"
└──────────┘


## Tool Orchestration Example

User: "I don't understand Bayes theorem"

┌─────────────────────────────────────────────────────────┐
│  Claude Sonnet 4 Decision Tree                          │
│                                                         │
│  1. Call search_knowledge_base                          │
│     → chunk_type="explanation"                          │
│     → "Bayes theorem"                                   │
│     ✓ Got explanation                                   │
│                                                         │
│  2. Call get_prerequisites                              │
│     → "Bayes theorem"                                   │
│     ✓ Got: conditional probability, independence        │
│                                                         │
│  3. Call search_knowledge_base                          │
│     → chunk_type="analogy"                              │
│     → "Bayes theorem"                                   │
│     ✓ Got relatable analogy                             │
│                                                         │
│  4. Call search_knowledge_base                          │
│     → chunk_type="worked_solution"                      │
│     → "Bayes theorem"                                   │
│     ✓ Got step-by-step example                          │
│                                                         │
│  5. Synthesize all content into comprehensive response  │
│     • Start with prerequisites check                    │
│     • Present explanation                               │
│     • Use analogy to clarify                            │
│     • Show worked example                               │
│     • Offer practice problems                           │
└─────────────────────────────────────────────────────────┘


## Configuration Flow

.env file
   │
   ▼
┌──────────────────────┐
│  RAGChatConfig       │
│  (config.py)         │
│                      │
│  • AWS_REGION        │
│  • MODEL_ID          │
│  • RAG_DB_PATH       │
│  • KEYWORDS_FILE     │
│  • NER_MODEL_PATH    │
│  • DEFAULT_K         │
│  • VERBOSE           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  RAGChatAgent        │
│  (agent.py)          │
│                      │
│  Uses config to:     │
│  • Create model      │
│  • Init RAG system   │
│  • Init keyword ex   │
│  • Set parameters    │
└──────────────────────┘


## Component Dependencies

┌─────────────────────────────────────┐
│  External Dependencies              │
│                                     │
│  • strands - Agent framework        │
│  • boto3 - AWS Bedrock access       │
│  • chromadb - Vector database       │
│  • dspy - Metadata extraction       │
│  • sentence-transformers - Embed    │
│  • spacy - NER                      │
│  • rapidfuzz - Fuzzy matching       │
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Internal Dependencies              │
│                                     │
│  • rag/rag_system.py                │
│  • rag/schema.py                    │
│  • keyword_extractor/               │
│    keyword_extractor.py             │
│  • keyword_extractor/               │
│    math_keyword_extractor.py        │
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  RAG Chat Agent                     │
│                                     │
│  • agents/rag_chat/__init__.py      │
│  • agents/rag_chat/agent.py         │
│  • agents/rag_chat/config.py        │
│  • agents/rag_chat/prompts.py       │
│  • agents/rag_chat/tools.py         │
└─────────────────────────────────────┘


## Multi-Agent System Integration

┌──────────────────────────────────────────────────────────┐
│               Orchestrator                               │
│                                                          │
│  Routes queries to specialized agents:                   │
│                                                          │
│  ┌────────────────┐  ┌────────────────┐               │
│  │  Onboarding    │  │  RAG Chat      │               │
│  │  Agent         │  │  Agent         │               │
│  │                │  │                │               │
│  │ • Assessments  │  │ • Tutoring     │               │
│  │ • Placement    │  │ • Content      │               │
│  │               │  │   retrieval    │               │
│  └────────────────┘  └────────────────┘               │
│                                                          │
│  ┌────────────────┐  ┌────────────────┐               │
│  │  Content Gen   │  │  Other         │               │
│  │  Agent         │  │  Agents...     │               │
│  │                │  │                │               │
│  │ • Generation   │  │ • ...          │               │
│  │ • Adaptation   │  │                │               │
│  └────────────────┘  └────────────────┘               │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Shared Memory   │
              │  • User profiles │
              │  • Context       │
              │  • History       │
              └──────────────────┘


## Memory and State Management

┌─────────────────────────────────────────────┐
│  Strands Agent (Built-in)                   │
│                                             │
│  • Conversation history                     │
│  • Tool call history                        │
│  • Context window management                │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  RAGChatTools (Singleton)                   │
│                                             │
│  • RAG system instance (persistent)         │
│  • Keyword extractor (persistent)           │
│  • Metadata extractor (persistent)          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  ChromaDB (Persistent)                      │
│                                             │
│  • Vector embeddings                        │
│  • Metadata                                 │
│  • Stored on disk                           │
└─────────────────────────────────────────────┘
```

This architecture provides:
- **Separation of concerns**: Clear boundaries between components
- **Scalability**: Singleton pattern for backend systems
- **Flexibility**: Easy to extend with new tools
- **Integration**: Works with orchestrator and other agents
- **Persistence**: ChromaDB and conversation memory
- **Observability**: Logging at each layer
