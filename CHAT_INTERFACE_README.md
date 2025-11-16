# Chat Interface for Learning Management System

Complete chat interface implementation with support for both orchestrator-mediated interactions and direct agent connections.

## 🏗️ Architecture

### **Two Connection Modes**

#### **1. Orchestrator Mode (Default)**
- User sends queries to orchestrator
- Orchestrator delegates to appropriate agents
- Used for general learning questions, content generation, learning paths
- Transparent agent routing

#### **2. Direct Agent Mode (Onboarding)**
- Direct connection to OnboardingAgent
- Used for sequential quiz interactions
- Bypasses orchestrator for performance
- Automatically switches to orchestrator after completion

### **System Components**

```
┌─────────────────┐
│  Chat Frontend  │  (React/Next.js)
│  Port: 3001     │
└────────┬────────┘
         │
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│   API Server    │  (FastAPI)
│   Port: 8000    │
└────────┬────────┘
         │
         ├─────────────┬─────────────┐
         ▼             ▼             ▼
   Orchestrator   Onboarding    Other Agents
      Agent         Agent

```

## 📁 Project Structure

```
api_server/
├── main.py                 # FastAPI server with REST + WebSocket
└── requirements.txt        # Python dependencies

chat_frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx       # Main page (routing logic)
│   │   ├── layout.tsx     # Root layout
│   │   └── globals.css    # Global styles
│   ├── components/
│   │   ├── WelcomeScreen.tsx      # Initial screen (mode selection)
│   │   ├── ChatInterface.tsx      # Main chat container
│   │   ├── Header.tsx             # Chat header with status
│   │   ├── MessageList.tsx        # Message display
│   │   ├── MessageBubble.tsx      # Individual message
│   │   ├── MessageInput.tsx       # Input area
│   │   └── TypingIndicator.tsx    # Typing animation
│   └── lib/
│       └── api.ts          # API client functions
├── package.json
├── next.config.js
├── tsconfig.json
└── tailwind.config.js
```

## 🚀 Quick Start

### **Prerequisites**

- Python 3.9+
- Node.js 18+
- npm or pnpm
- AWS credentials configured (for Bedrock)

### **1. Start API Server**

```bash
cd api_server

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

API will be available at:
- REST: http://localhost:8000
- WebSocket: ws://localhost:8000/ws/{session_id}
- Docs: http://localhost:8000/docs

### **2. Start Chat Frontend**

```bash
cd chat_frontend

# Install dependencies
npm install
# or
pnpm install

# Create environment file
cp .env.local.example .env.local

# Start development server
npm run dev
# or
pnpm dev
```

Frontend will be available at: http://localhost:3001

## 🔌 API Endpoints

### **REST Endpoints**

#### **Create Session**
```http
POST /api/sessions
Content-Type: application/json

{
  "user_id": "student123",
  "mode": "orchestrator"  // or "onboarding"
}

Response:
{
  "session_id": "uuid",
  "user_id": "student123",
  "mode": "orchestrator",
  "message": "Session created in orchestrator mode"
}
```

#### **Send Message**
```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "uuid",
  "message": "What is probability?",
  "context": {}  // optional
}

Response:
{
  "session_id": "uuid",
  "response": "Probability is...",
  "agent": "Orchestrator",
  "mode": "orchestrator",
  "metadata": {}
}
```

#### **Get Session Info**
```http
GET /api/sessions/{session_id}

Response:
{
  "session_id": "uuid",
  "user_id": "student123",
  "mode": "orchestrator",
  "current_agent": "OnboardingAgent",
  "message_count": 10,
  "has_profile": true
}
```

#### **Get Conversation History**
```http
GET /api/sessions/{session_id}/history

Response:
{
  "session_id": "uuid",
  "history": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

#### **Get User Profile**
```http
GET /api/users/{user_id}/profile

Response:
{
  "user_id": "student123",
  "has_profile": true,
  "profile": {
    "competence_level": "intermediate",
    "ability_score": 0.45,
    ...
  }
}
```

### **WebSocket Connection**

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/{session_id}')

// Send message
ws.send(JSON.stringify({
  message: "What is probability?"
}))

// Receive messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  
  switch (data.type) {
    case 'connected':
      // Connection established
      break
    case 'typing':
      // Agent is typing
      break
    case 'message':
      // Message received
      console.log(data.content)
      break
    case 'error':
      // Error occurred
      console.error(data.message)
      break
  }
}
```

## 🎨 Frontend Features

### **Welcome Screen**
- User ID input
- Mode selection (onboarding vs chat)
- Profile detection (skips onboarding if complete)

### **Chat Interface**
- Real-time WebSocket communication
- Message history
- Typing indicators
- Markdown support with math rendering (KaTeX)
- Syntax highlighting for code
- Agent attribution badges
- Connection status indicator
- Session management

### **Message Input**
- Auto-resizing textarea
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)
- Character counter
- Disabled state during processing
- Mode-specific placeholders

## 🔄 User Flow

### **New User Flow (with Onboarding)**

1. User arrives at welcome screen
2. Enters user ID, selects "Start with Assessment"
3. Creates session in `onboarding` mode
4. Takes adaptive quiz (direct connection to OnboardingAgent)
5. Quiz completes → UserProfile created
6. Mode automatically switches to `orchestrator`
7. Continues with general chat

### **Returning User Flow**

1. User arrives at welcome screen
2. Enters user ID, selects "Start Chatting"
3. System checks for existing profile
4. Creates session in `orchestrator` mode
5. Interacts with orchestrator (delegates to agents as needed)

### **Forced Onboarding for New Users**

If user tries to use orchestrator mode without profile:
1. Orchestrator detects missing profile
2. Returns message: "You need to complete onboarding first"
3. Frontend can redirect to onboarding mode

## 🛠️ Development

### **Environment Variables**

**API Server:**
```bash
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1

# Optional: Quiz Configuration
TOTAL_QUESTIONS=25
```

**Frontend:**
```bash
# API endpoints
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### **Running in Production**

**API Server:**
```bash
# Using uvicorn with workers
uvicorn api_server.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or with gunicorn
gunicorn api_server.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Frontend:**
```bash
# Build for production
npm run build

# Start production server
npm start
```

## 🧪 Testing

### **Test API Server**

```bash
# Health check
curl http://localhost:8000/

# Create session
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test123", "mode": "orchestrator"}'

# Send message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "YOUR_SESSION_ID", "message": "Hello"}'
```

### **Test WebSocket**

Use the interactive docs at http://localhost:8000/docs or test with:

```javascript
// In browser console
const ws = new WebSocket('ws://localhost:8000/ws/YOUR_SESSION_ID')
ws.onmessage = (e) => console.log(JSON.parse(e.data))
ws.send(JSON.stringify({ message: "Hello!" }))
```

## 📝 Session Management

- **In-Memory Storage**: Sessions stored in memory (use Redis for production)
- **Session ID**: UUID generated for each session
- **Conversation History**: Stored per session
- **User Profiles**: Shared across sessions for same user
- **Agent State**: Persistent per session (e.g., quiz progress)

## 🔐 Security Considerations

For production deployment:

1. **CORS**: Configure `allow_origins` to specific domains
2. **Authentication**: Add auth middleware for API endpoints
3. **Rate Limiting**: Implement rate limiting on endpoints
4. **WebSocket Auth**: Validate session IDs before accepting connections
5. **Input Validation**: Already using Pydantic models
6. **Environment Variables**: Never commit credentials

## 🚧 Future Enhancements

- [ ] Implement actual Orchestrator agent (currently placeholder)
- [ ] Add Redis for session persistence
- [ ] Implement authentication system
- [ ] Add file upload support
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Export conversation history
- [ ] Rich media support (images, videos)
- [ ] Mobile responsive design improvements
- [ ] Offline mode support

## 🐛 Troubleshooting

### **WebSocket Connection Fails**

- Check if API server is running
- Verify session ID is valid
- Check browser console for errors
- Ensure no CORS issues

### **Messages Not Sending**

- Verify WebSocket connection status (green indicator)
- Check if input is not empty
- Look for errors in browser console
- Check API server logs

### **Onboarding Not Starting**

- Ensure user hasn't completed onboarding already
- Check AWS credentials are set
- Verify Bedrock access in configured region
- Check API server logs for errors

### **Frontend Won't Start**

- Run `npm install` or `pnpm install`
- Check Node.js version (18+)
- Verify `.env.local` file exists
- Clear `.next` cache: `rm -rf .next`

## 📚 Related Documentation

- [Onboarding Agent README](../ONBOARDING_AGENT_README.md)
- [Implementation Summary](../IMPLEMENTATION_SUMMARY.md)
- [Quick Start Guide](../QUICK_START.md)

## 📧 Support

For issues or questions, refer to the main project documentation or check the API interactive docs at http://localhost:8000/docs
