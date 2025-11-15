# 🎓 Learning Management Assistant - Complete System

## 🌟 Overview

A comprehensive AI-powered learning management system with:
- **Adaptive Assessment**: IRT-based onboarding quiz to determine student competence
- **Agentic Architecture**: Strands Agent framework with orchestrator pattern
- **Chat Interface**: Modern React/Next.js frontend with WebSocket support
- **Dual Connection Modes**: Orchestrator-mediated + direct agent connections

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                              │
│  ┌──────────────────────┐     ┌──────────────────────┐          │
│  │  Welcome Screen      │ →   │  Chat Interface      │          │
│  │  (Mode Selection)    │     │  (Real-time Chat)    │          │
│  └──────────────────────┘     └──────────────────────┘          │
│              Next.js Frontend (Port 3001)                        │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API SERVER                                  │
│  ┌────────────────────────────────────────────────┐             │
│  │  Session Manager  │  WebSocket Handler         │             │
│  │  REST Endpoints   │  Connection Manager        │             │
│  └────────────────────────────────────────────────┘             │
│              FastAPI Server (Port 8000)                          │
└───────────────────────────┬──────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┬─────────────┐
              ▼                           ▼             ▼
┌──────────────────────┐    ┌──────────────────────┐   │
│   ORCHESTRATOR       │    │   ONBOARDING AGENT   │   │
│   (Planned)          │    │   (Implemented)      │   │
│                      │    │                      │   │
│  - Delegates tasks   │    │  - Adaptive quiz     │   │
│  - Shared memory     │    │  - IRT algorithm     │   │
│  - Agent routing     │    │  - Profile creation  │   │
└──────────────────────┘    └──────────────────────┘   │
                                                        ▼
                                          ┌──────────────────────┐
                                          │   OTHER AGENTS       │
                                          │   (Future)           │
                                          │                      │
                                          │  - Content Gen       │
                                          │  - Learning Path     │
                                          │  - Q&A              │
                                          └──────────────────────┘
```

## 📦 Components

### **1. Onboarding Quiz (Original - FastAPI + Next.js)**
- Location: `onboarding/backend/`, `onboarding/frontend/`
- Standalone adaptive quiz system
- 73+ probability questions
- SQLite database
- IRT-based ability estimation

### **2. Onboarding Agent (Strands Framework)**
- Location: `agents/onboarding/`
- Wraps existing quiz logic with Strands @tool decorators
- AWS Bedrock (Claude Sonnet 4) integration
- Creates `UserProfile` for orchestrator memory
- CLI interface for testing

### **3. API Server (FastAPI)**
- Location: `api_server/`
- REST + WebSocket endpoints
- Session management
- Routes to orchestrator or direct agents
- Real-time communication

### **4. Chat Frontend (Next.js)**
- Location: `chat_frontend/`
- Modern React UI with TypeScript
- WebSocket real-time updates
- Markdown + math rendering (KaTeX)
- Mode switching (onboarding ↔ orchestrator)

## 🚀 Quick Start

### **Prerequisites**
```bash
# Check versions
python --version    # 3.9+
node --version      # 18+
npm --version

# AWS credentials
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### **One-Command Setup**
```bash
# Run setup script
./setup_chat_interface.sh
```

### **Manual Start**

**Terminal 1 - API Server:**
```bash
cd api_server
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Chat Frontend:**
```bash
cd chat_frontend
npm install
npm run dev
```

**Access:**
- Frontend: http://localhost:3001
- API Docs: http://localhost:8000/docs

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CHAT_INTERFACE_README.md](./CHAT_INTERFACE_README.md) | Complete chat interface guide |
| [ONBOARDING_AGENT_README.md](./ONBOARDING_AGENT_README.md) | Strands agent implementation |
| [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) | Technical decisions & architecture |
| [QUICK_START.md](./QUICK_START.md) | Quick reference guide |
| [onboarding/INSTRUCTIONS.md](./onboarding/INSTRUCTIONS.md) | Original quiz system |

## 🔄 User Flows

### **New User (First Time)**

1. **Welcome Screen**
   - Enter user ID: `student123`
   - Select: "Start with Assessment"

2. **Onboarding Mode (Direct Connection)**
   - Connects directly to OnboardingAgent
   - Takes adaptive quiz (5-25 questions)
   - Questions adapt based on answers
   - System estimates ability using IRT

3. **Profile Creation**
   - UserProfile created with competence level
   - Stored in orchestrator memory
   - Contains: ability score, competence level, performance metrics

4. **Auto-Switch to Chat Mode**
   - Mode switches from `onboarding` → `orchestrator`
   - User continues with general chat
   - Orchestrator has access to profile

### **Returning User**

1. **Welcome Screen**
   - Enter user ID: `student123`
   - Select: "Start Chatting"

2. **Orchestrator Mode**
   - System detects existing profile
   - Skips onboarding
   - Routes queries through orchestrator
   - Orchestrator delegates to appropriate agents

## 🛠️ Development

### **Project Structure**
```
lma-major-project-moya-moye/
├── agents/
│   └── onboarding/              # Strands onboarding agent
│       ├── agent.py
│       ├── tools.py
│       ├── config.py
│       └── prompts.py
├── shared/
│   └── models.py                # UserProfile dataclass
├── api_server/
│   ├── main.py                  # FastAPI server
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
├── run_onboarding_agent.py      # CLI for testing agent
├── example_orchestrator.py       # Example orchestrator
├── setup_chat_interface.sh       # Setup script
├── start-api-server.sh           # Start API
└── start-chat-frontend.sh        # Start frontend
```

### **Environment Variables**

**API Server (.env or export):**
```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1

# Quiz config
TOTAL_QUESTIONS=25  # Default number of questions
```

**Frontend (chat_frontend/.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### **Testing**

**Test Onboarding Agent (CLI):**
```bash
python run_onboarding_agent.py --questions 5 --user-id test123
```

**Test API Server:**
```bash
# Create session
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test123", "mode": "onboarding"}'

# Send message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "YOUR_SESSION_ID", "message": "start"}'
```

**Test Original Quiz:**
```bash
cd onboarding
./start-backend.sh   # Terminal 1
./start-frontend.sh  # Terminal 2
# Open: http://localhost:3000
```

## 🎯 Connection Modes Explained

### **When to Use Orchestrator Mode**
- ✅ General questions about probability
- ✅ Requesting learning paths
- ✅ Asking for content generation
- ✅ Complex queries requiring multiple agents
- ✅ User has completed onboarding

**How it works:**
```
User → Frontend → API → Orchestrator → [Agent Selection] → Response
```

### **When to Use Direct Agent Mode (Onboarding)**
- ✅ Taking initial assessment
- ✅ Sequential quiz interactions
- ✅ No profile exists yet
- ✅ Performance-critical flows

**How it works:**
```
User → Frontend → API → OnboardingAgent (direct) → Response
```

**Automatic switching:**
```
Onboarding Complete → Profile Created → Auto-switch to Orchestrator
```

## 🔌 API Reference

### **REST Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/sessions` | POST | Create new session |
| `/api/sessions/{id}` | GET | Get session info |
| `/api/sessions/{id}/history` | GET | Get conversation history |
| `/api/users/{id}/profile` | GET | Get user profile |
| `/api/chat` | POST | Send message (REST) |

### **WebSocket**

```javascript
ws://localhost:8000/ws/{session_id}

// Message types:
// - connected: Connection established
// - typing: Agent is typing
// - message: Agent response
// - error: Error occurred
```

## 🧪 Example Usage

### **Python (API Client)**
```python
import requests

# Create session
response = requests.post('http://localhost:8000/api/sessions', json={
    'user_id': 'student123',
    'mode': 'onboarding'
})
session = response.json()
session_id = session['session_id']

# Send message
response = requests.post('http://localhost:8000/api/chat', json={
    'session_id': session_id,
    'message': 'start'
})
print(response.json()['response'])
```

### **JavaScript (WebSocket)**
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`)

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  if (data.type === 'message') {
    console.log('Response:', data.content)
  }
}

ws.send(JSON.stringify({ message: 'What is probability?' }))
```

## 📊 Data Models

### **UserProfile**
```python
@dataclass
class UserProfile:
    user_id: str
    competence_level: str           # "beginner", "intermediate", "advanced"
    ability_score: float            # -3.0 to 3.0 (IRT scale)
    correct_answers: int
    total_questions: int
    average_response_time: float
    topics_mastered: List[str]
    topics_to_review: List[str]
    recommended_starting_level: str
    # ... 20+ fields total
```

### **Message**
```typescript
interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  metadata?: {
    agent?: string
    quiz_active?: boolean
    mode_switched?: boolean
  }
}
```

## 🚧 Future Enhancements

### **Immediate (In Progress)**
- [ ] Implement full Orchestrator agent
- [ ] Add more agents (Content Generator, Learning Path)
- [ ] Redis for session persistence

### **Short Term**
- [ ] Authentication system
- [ ] User dashboard
- [ ] Progress tracking
- [ ] Export quiz results
- [ ] Multi-topic support

### **Long Term**
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Collaborative learning
- [ ] Gamification
- [ ] Analytics dashboard

## 🔧 Troubleshooting

### **Common Issues**

**"WebSocket connection failed"**
- Ensure API server is running (`python api_server/main.py`)
- Check session ID is valid
- Verify port 8000 is not blocked

**"AWS Bedrock error"**
- Confirm AWS credentials are set
- Check region is `us-east-1`
- Verify Bedrock access in IAM

**"Session not found"**
- Session may have expired (in-memory storage)
- Create new session
- Consider Redis for production

**"Frontend won't start"**
- Run `npm install` in chat_frontend/
- Check Node.js version (18+)
- Clear Next.js cache: `rm -rf .next`

## 📈 Performance

- **WebSocket latency**: < 100ms typical
- **Agent response time**: 2-5 seconds (depends on LLM)
- **Quiz completion**: 5-10 minutes (adaptive)
- **Frontend load time**: < 2 seconds

## 🔒 Security Notes

- Environment variables for secrets (never commit)
- Pydantic validation on all inputs
- CORS configuration needed for production
- Add authentication middleware for production
- Rate limiting recommended

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines]

## 📧 Contact

[Add contact information]

---

**Ready to start?**
```bash
./setup_chat_interface.sh
./start-api-server.sh      # Terminal 1
./start-chat-frontend.sh   # Terminal 2
```

Then open: **http://localhost:3001** 🚀
