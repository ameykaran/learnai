# Learning Management Assistant (LMA)

A comprehensive AI-powered learning management system with adaptive assessment, agentic architecture, and modern chat interface.

> 🚀 **NEW**: Complete chat interface with orchestrator + direct agent support now available!

## 🌟 Quick Links

- **[Complete System Guide](./COMPLETE_SYSTEM_README.md)** - Full documentation
- **[Chat Interface](./CHAT_INTERFACE_README.md)** - Frontend + API server
- **[Onboarding Agent](./ONBOARDING_AGENT_README.md)** - Strands agent implementation
- **[Quick Start](./QUICK_START.md)** - Get started in 5 minutes

## Overview

LMA is a multi-agent learning system that combines adaptive assessment with AI-powered tutoring. It includes:

1. **Adaptive Onboarding Quiz**: IRT-based assessment to determine student competence
2. **Agentic Architecture**: Strands Agent framework with orchestrator pattern
3. **Chat Interface**: Modern React/Next.js frontend with real-time communication
4. **Dual Connection Modes**: Orchestrator-mediated + direct agent connections
5. **Document Processing**: Self-adaptive pipeline for mathematical content extraction

![AGENT2026-lma](https://github.com/user-attachments/assets/525eb135-af69-45a1-bbf7-93a522704fad)

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone [your-repo]
cd lma-major-project-moya-moye
./setup_chat_interface.sh

# 2. Set AWS credentials
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# 3. Start API server (Terminal 1)
./start-api-server.sh

# 4. Start frontend (Terminal 2)
./start-chat-frontend.sh

# 5. Open http://localhost:3001
```

## 🎯 Key Features

### **Learning System**
- **Adaptive Assessment**: IRT-based quiz determines student competence level
- **Strands Agent Framework**: Tool-based agentic architecture with AWS Bedrock
- **Dual Connection Modes**: Orchestrator-mediated or direct agent connections
- **Real-time Chat**: WebSocket communication with typing indicators
- **Math Support**: KaTeX rendering for mathematical notation

### **Document Processing**
- **Self-Adaptive Pipeline**: Chooses optimal processing (Marker vs OCR)
- **Mathematical Notation**: Preserves LaTeX formatting
- **Custom NER Model**: Trained on 500+ probability terms
- **Hybrid RAG**: Semantic search + metadata filtering
- **Cost Optimization**: 15-30% reduction in processing costs

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHAT FRONTEND (Next.js)                       │
│  ┌────────────────┐    ┌──────────────────────────────────┐    │
│  │ Welcome Screen │ →  │  Chat Interface (WebSocket)      │    │
│  └────────────────┘    └──────────────────────────────────┘    │
│                         Port 3001                                │
└──────────────────────────────┬───────────────────────────────────┘
                               │ HTTP/WebSocket
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API SERVER (FastAPI)                          │
│  Session Management • WebSocket Handler • REST Endpoints        │
│                         Port 8000                                │
└──────────────────────────────┬───────────────────────────────────┘
                               │
              ┌────────────────┴─────────────┬──────────┐
              ▼                              ▼          ▼
    ┌──────────────────┐         ┌──────────────────┐  │
    │  ORCHESTRATOR    │         │  ONBOARDING      │  │
    │  (Planned)       │         │  AGENT           │  │
    │                  │         │  (Strands)       │  │
    │  • Delegates     │         │  • Adaptive Quiz │  │
    │  • Shared Memory │         │  • IRT Algorithm │  │
    └──────────────────┘         └──────────────────┘  │
                                                        ▼
                                           ┌──────────────────┐
                                           │  FUTURE AGENTS   │
                                           │  • Content Gen   │
                                           │  • Learning Path │
                                           └──────────────────┘
```

### **Dual Connection Modes**

1. **Orchestrator Mode**: For general queries, delegates to appropriate agents
2. **Direct Agent Mode**: For sequential flows like onboarding quiz

## 📁 Project Structure

```
lma-major-project-moya-moye/
├── agents/
│   └── onboarding/              # Strands onboarding agent
├── shared/
│   └── models.py                # UserProfile dataclass
├── api_server/
│   ├── main.py                  # FastAPI server (REST + WebSocket)
│   └── requirements.txt
├── chat_frontend/
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   ├── components/          # React components
│   │   └── lib/                 # API client
│   └── package.json
├── onboarding/
│   ├── backend/                 # Original FastAPI quiz
│   └── frontend/                # Original Next.js UI
├── ocr_chunks/                  # Document processing
├── rag/                         # RAG system
├── keyword_extractor/           # Custom NER model
├── run_onboarding_agent.py      # CLI for agent testing
├── example_orchestrator.py      # Example orchestrator
├── setup_chat_interface.sh      # Setup script
├── start-api-server.sh          # Start API
└── start-chat-frontend.sh       # Start frontend
```


## 💻 Technology Stack

### **Frontend**
- Next.js 14 with TypeScript
- React 18 with hooks
- Tailwind CSS for styling
- WebSocket for real-time updates
- React Markdown with KaTeX

### **Backend**
- FastAPI with WebSocket support
- Strands Agent framework
- AWS Bedrock (Claude Sonnet 4)
- SQLite for quiz data
- Pydantic for validation

### **ML/AI**
- IRT algorithm for adaptive testing
- Custom NER model (SpaCy)
- Google Gemini 2.5 Flash
- DSPy for structured outputs
- ChromaDB for vector storage

### **Document Processing**
- Marker library for PDF parsing
- OCR pipeline for images
- RapidFuzz for fuzzy matching
- ThreadPoolExecutor for parallel processing

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [COMPLETE_SYSTEM_README.md](./COMPLETE_SYSTEM_README.md) | Full system documentation |
| [CHAT_INTERFACE_README.md](./CHAT_INTERFACE_README.md) | Chat frontend + API guide |
| [ONBOARDING_AGENT_README.md](./ONBOARDING_AGENT_README.md) | Strands agent implementation |
| [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) | Technical decisions |
| [QUICK_START.md](./QUICK_START.md) | Quick reference |
| [onboarding/INSTRUCTIONS.md](./onboarding/INSTRUCTIONS.md) | Original quiz system |

## 🔄 User Flows

### **New User Journey**
1. Enter user ID on welcome screen
2. Select "Start with Assessment"
3. Take adaptive quiz (5-25 questions)
4. System creates UserProfile
5. Auto-switch to chat mode
6. Continue with personalized learning

### **Returning User Journey**
1. Enter user ID on welcome screen
2. Select "Start Chatting"
3. System loads existing profile
4. Chat with orchestrator
5. Orchestrator delegates to agents as needed

## Data Schema

Each processed chunk follows this structure:

```python
{
    "text": str,
    "metadata": {
        "source_url": str,
        "source_type": str,
        "topics": List[str],
        "subtopics": List[str],
        "chunk_type": Literal["definition", "example", "explanation",
                             "proof", "visualization", "practice_problem",
                             "worked_solution", "analogy", "misconception"],
        "difficulty_level": Literal["basic", "intermediate", "advanced"],
        "prerequisites": List[str]
    }
}
```

## Results

- **Token Efficiency**: 15-30% cost reduction through adaptive pipeline selection
- **Mathematical Preservation**: 95% accuracy in LaTeX formula extraction
- **NER Performance**: 91% accuracy in keyword extraction
- **Processing Speed**: Parallel processing with configurable worker threads

## Demo Output

```bash
Query: 'Explain the concept of conditional probability.'
Input Filters: {'topics': ['conditional probability', 'probability'],
                'chunk_type': 'explanation'}
Found 3 results.
Retrieved Chunks:

Source Type: textbook, Chunk Type: explanation
Content: ## 13.2.1 Properties of conditional probability...
Topics: ['conditional probability', 'properties of probability', 'sample space']
```

## Future Work

Post mid-evaluation deliverables will include:
- Core SME capabilities (quiz generation, dynamic learning modules)
- Conversational agents with multi-step reasoning workflows - Integration with MOYA
- Tool-using capabilities (document generation, email automation)
- Hybrid retrieval mechanisms combining vector search with BM25
- Guardrails for input sanitization and output moderation
- Modular API servers with FastAPI

## Research Context

This work builds upon the DeepSeek-OCR research findings, which demonstrated 97% OCR precision at 10× compression ratios. Our adaptive approach leverages these insights to optimize processing costs while maintaining mathematical accuracy.

## Future Integration

The current implementation serves as a proof-of-concept for integration with the MOYA multiagent framework - an engineering LLM-powered multiagent system for autonomous operations. MOYA will provide the architectural foundation for scaling this approach to handle diverse educational materials simultaneously.

## Contributors

- Sreemaee Akshathala (2025701028)
- Amey Karan (2022111026)
