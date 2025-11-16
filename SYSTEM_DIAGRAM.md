# System Architecture Diagram

## Complete Chat Interface System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                            USER BROWSER                                     │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                       │ │
│  │                      WELCOME SCREEN                                   │ │
│  │                                                                       │ │
│  │   ┌─────────────────────────────────────────────────┐                │ │
│  │   │  Enter User ID: [_______________]               │                │ │
│  │   │                                                  │                │ │
│  │   │  ┌────────────────────┐  ┌────────────────────┐ │                │ │
│  │   │  │ 📝 Start with      │  │ 💬 Start           │ │                │ │
│  │   │  │    Assessment      │  │    Chatting        │ │                │ │
│  │   │  └────────────────────┘  └────────────────────┘ │                │ │
│  │   └─────────────────────────────────────────────────┘                │ │
│  │                              │                                        │ │
│  └──────────────────────────────┼────────────────────────────────────────┘ │
│                                 │                                          │
│                                 ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                       │ │
│  │                      CHAT INTERFACE                                   │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ 🎓 Learning Assistant    User: student123    ● Connected       │ │ │
│  │  │ Mode: 📝 Assessment / 💬 Chat                                  │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │                                                                 │ │ │
│  │  │  Assistant: Welcome! Ready to start assessment?                 │ │ │
│  │  │                                                                 │ │ │
│  │  │                                         User: yes, let's start  │ │ │
│  │  │                                                                 │ │ │
│  │  │  Assistant: Question 1: What is probability?                   │ │ │
│  │  │                                                                 │ │ │
│  │  │                                    User: It's a measure of...   │ │ │
│  │  │                                                                 │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ [Type your message...]                              [Send ➤]    │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                              Next.js (Port 3001)                          │
│                                      │                                    │
└──────────────────────────────────────┼────────────────────────────────────┘
                                       │
                                       │ HTTP / WebSocket
                                       │
┌──────────────────────────────────────▼────────────────────────────────────┐
│                                                                            │
│                          API SERVER (FastAPI)                              │
│                            Port 8000                                       │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                      SESSION MANAGER                                 │ │
│  │                                                                      │ │
│  │  sessions: {                                                         │ │
│  │    "uuid-1": {                                                       │ │
│  │      user_id: "student123",                                         │ │
│  │      mode: "onboarding",                                            │ │
│  │      conversation_history: [...],                                   │ │
│  │      agent_state: {...}                                             │ │
│  │    }                                                                 │ │
│  │  }                                                                   │ │
│  │                                                                      │ │
│  │  user_profiles: {                                                    │ │
│  │    "student123": UserProfile(...)                                   │ │
│  │  }                                                                   │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                   CONNECTION MANAGER                                 │ │
│  │                                                                      │ │
│  │  WebSocket Connections:                                              │ │
│  │  ├─ session-uuid-1 → WebSocket (connected)                          │ │
│  │  ├─ session-uuid-2 → WebSocket (connected)                          │ │
│  │  └─ session-uuid-3 → WebSocket (connected)                          │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                      API ENDPOINTS                                   │ │
│  │                                                                      │ │
│  │  POST   /api/sessions              → Create session                 │ │
│  │  GET    /api/sessions/{id}         → Get session info               │ │
│  │  GET    /api/sessions/{id}/history → Get messages                   │ │
│  │  GET    /api/users/{id}/profile    → Get user profile               │ │
│  │  POST   /api/chat                  → Send message                   │ │
│  │  WS     /ws/{session_id}           → WebSocket connection           │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                      │                                    │
└──────────────────────────────────────┼────────────────────────────────────┘
                                       │
                ┌──────────────────────┴───────────────────┐
                │                                          │
                ▼                                          ▼
┌───────────────────────────────┐          ┌──────────────────────────────┐
│                               │          │                              │
│    ORCHESTRATOR AGENT         │          │    ONBOARDING AGENT         │
│    (Planned/Placeholder)      │          │    (Strands Framework)      │
│                               │          │                              │
│  ┌─────────────────────────┐  │          │  ┌────────────────────────┐ │
│  │ Decision Logic:         │  │          │  │ Tools:                 │ │
│  │                         │  │          │  │                        │ │
│  │ • Check user profile    │  │          │  │ @tool                  │ │
│  │ • Analyze query intent  │  │          │  │ start_assessment()     │ │
│  │ • Route to agent        │  │          │  │                        │ │
│  │                         │  │          │  │ @tool                  │ │
│  │ Delegates to:           │  │          │  │ get_next_question()    │ │
│  │ ├─ OnboardingAgent      │  │          │  │                        │ │
│  │ ├─ ContentGenerator     │  │          │  │ @tool                  │ │
│  │ ├─ LearningPathAgent    │  │          │  │ submit_answer()        │ │
│  │ └─ Q&A Agent            │  │          │  │                        │ │
│  └─────────────────────────┘  │          │  │ @tool                  │ │
│                               │          │  │ get_progress()         │ │
│  Shared Memory:               │          │  │                        │ │
│  ├─ UserProfiles             │          │  │ @tool                  │ │
│  ├─ Learning History         │          │  │ finalize_assessment()  │ │
│  └─ Context                  │          │  └────────────────────────┘ │
│                               │          │                              │
└───────────────────────────────┘          │  ┌────────────────────────┐ │
                                           │  │ Backend:               │ │
                                           │  │                        │ │
                                           │  │ • SQLite Database      │ │
                                           │  │ • IRT Algorithm        │ │
                                           │  │ • 73+ Questions        │ │
                                           │  │ • Adaptive Selection   │ │
                                           │  └────────────────────────┘ │
                                           │                              │
                                           │  ┌────────────────────────┐ │
                                           │  │ AWS Bedrock:           │ │
                                           │  │                        │ │
                                           │  │ • Claude Sonnet 4      │ │
                                           │  │ • us-east-1            │ │
                                           │  └────────────────────────┘ │
                                           │                              │
                                           │  Creates: UserProfile        │
                                           │  ├─ competence_level         │
                                           │  ├─ ability_score            │
                                           │  ├─ correct_answers          │
                                           │  └─ recommended_level        │
                                           │                              │
                                           └──────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                         CONNECTION MODES                                   │
│                                                                            │
│  MODE 1: ORCHESTRATOR (Default)                                           │
│  ───────────────────────────────────────                                  │
│  User → Frontend → API → Orchestrator → Agent → Response                  │
│                                                                            │
│  Use Cases:                                                                │
│  • General questions                                                       │
│  • Learning path requests                                                  │
│  • Content generation                                                      │
│  • Multi-agent coordination                                                │
│                                                                            │
│  MODE 2: DIRECT AGENT (Onboarding)                                        │
│  ────────────────────────────────────                                     │
│  User → Frontend → API → OnboardingAgent (direct) → Response              │
│                                                                            │
│  Use Cases:                                                                │
│  • Sequential quiz interactions                                            │
│  • Initial assessment                                                      │
│  • Performance-critical flows                                              │
│                                                                            │
│  Auto-Switch:                                                              │
│  Onboarding Complete → Profile Created → Switch to Orchestrator           │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                          DATA FLOW                                         │
│                                                                            │
│  1. USER ACTION                                                            │
│     User types: "start"                                                    │
│     ↓                                                                      │
│  2. FRONTEND                                                               │
│     WebSocket.send({ message: "start" })                                  │
│     ↓                                                                      │
│  3. API SERVER                                                             │
│     • Receive message                                                      │
│     • Get session info                                                     │
│     • Check mode (onboarding/orchestrator)                                 │
│     • Route to appropriate handler                                         │
│     ↓                                                                      │
│  4. AGENT                                                                  │
│     • OnboardingAgent.chat("start")                                       │
│     • start_assessment() tool                                              │
│     • get_next_question() tool                                             │
│     ↓                                                                      │
│  5. DATABASE                                                               │
│     • Fetch question from SQLite                                           │
│     • Apply IRT algorithm                                                  │
│     • Select adaptive difficulty                                           │
│     ↓                                                                      │
│  6. LLM (AWS Bedrock)                                                      │
│     • Format question naturally                                            │
│     • Add context and hints                                                │
│     ↓                                                                      │
│  7. RESPONSE                                                               │
│     API → WebSocket → Frontend → Display                                  │
│     "Question 1: What is the probability of..."                           │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│                                                                 │
│  Framework:   Next.js 14 (App Router)                          │
│  UI Library:  React 18                                         │
│  Language:    TypeScript                                       │
│  Styling:     Tailwind CSS                                     │
│  Real-time:   WebSocket API                                    │
│  Markdown:    react-markdown                                   │
│  Math:        KaTeX (rehype-katex)                             │
│  HTTP:        Fetch API                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       API SERVER                                │
│                                                                 │
│  Framework:   FastAPI                                          │
│  Language:    Python 3.9+                                      │
│  Validation:  Pydantic v2                                      │
│  WebSocket:   fastapi.websockets                               │
│  ASGI:        Uvicorn                                          │
│  CORS:        fastapi.middleware.cors                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AGENT FRAMEWORK                              │
│                                                                 │
│  Framework:   Strands Agents 1.0+                              │
│  LLM:         AWS Bedrock (Claude Sonnet 4)                    │
│  Tools:       @tool decorator pattern                          │
│  Backend:     SQLAlchemy 2.0                                   │
│  Database:    SQLite                                           │
│  Algorithm:   IRT (Item Response Theory)                       │
│  SDK:         boto3 (AWS)                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## File Organization

```
project-root/
│
├── api_server/               # FastAPI backend
│   ├── main.py              # Server + routes + WebSocket
│   └── requirements.txt     # Python dependencies
│
├── chat_frontend/           # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js pages
│   │   │   ├── page.tsx    # Main entry
│   │   │   ├── layout.tsx  # Root layout
│   │   │   └── globals.css # Styles
│   │   ├── components/     # React components
│   │   │   ├── WelcomeScreen.tsx
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── TypingIndicator.tsx
│   │   └── lib/
│   │       └── api.ts      # API client
│   └── package.json
│
├── agents/
│   └── onboarding/         # Strands agent
│       ├── agent.py        # OnboardingAgent class
│       ├── tools.py        # @tool functions
│       ├── config.py       # Configuration
│       └── prompts.py      # Instructions
│
├── shared/
│   └── models.py           # UserProfile dataclass
│
├── onboarding/             # Original quiz system
│   ├── backend/            # FastAPI
│   └── frontend/           # Next.js
│
└── Documentation/
    ├── START_HERE.md               # Quick start checklist
    ├── CHAT_INTERFACE_README.md    # Complete guide
    ├── COMPLETE_SYSTEM_README.md   # Full system
    ├── IMPLEMENTATION_COMPLETE.md  # Summary
    └── SYSTEM_DIAGRAM.md           # This file
```

## State Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION STATE                                │
│                                                                 │
│  Session {                                                      │
│    session_id: UUID                                            │
│    user_id: string                                             │
│    mode: "orchestrator" | "onboarding"                         │
│    created_at: datetime                                         │
│    current_agent: string | null                                │
│    conversation_history: Message[]                             │
│    agent_state: {                                              │
│      onboarding_agent?: OnboardingAgent instance               │
│      quiz_started?: boolean                                    │
│      current_question?: int                                    │
│    }                                                            │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    USER PROFILE                                 │
│                                                                 │
│  UserProfile {                                                  │
│    user_id: string                                             │
│    competence_level: "beginner" | "intermediate" | "advanced"  │
│    ability_score: float (-3.0 to 3.0)                          │
│    correct_answers: int                                        │
│    total_questions: int                                        │
│    average_response_time: float                                │
│    topics_mastered: string[]                                   │
│    topics_to_review: string[]                                  │
│    recommended_starting_level: string                          │
│    strengths: string[]                                         │
│    weaknesses: string[]                                        │
│    learning_style: string                                      │
│    quiz_session_id: string                                     │
│    completed_at: datetime                                      │
│    last_updated: datetime                                      │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
