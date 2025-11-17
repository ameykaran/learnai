# 🚀 Chat Interface - Quick Start Checklist

Use this checklist to get your chat interface running!

## ✅ Prerequisites

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm or pnpm installed (`npm --version`)
- [ ] AWS credentials configured

## 🔧 Setup Steps

### 1. Set AWS Credentials
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

- [ ] AWS credentials set
- [ ] Verify: `echo $AWS_ACCESS_KEY_ID` shows your key

### 2. Run Setup Script (Automatic)
```bash
cd /home/amey/Academics/LMA/lma-major-project-moya-moye
./setup_chat_interface.sh
```

- [ ] Setup script completed successfully
- [ ] No error messages displayed

### 3. Start API Server
```bash
# Terminal 1
./start-api-server.sh

# Should see:
# "Learning API Server Starting"
# "REST API: http://localhost:8000"
# "Docs: http://localhost:8000/docs"
```

- [ ] API server running
- [ ] Can access http://localhost:8000 (shows service status)
- [ ] Can access http://localhost:8000/docs (interactive docs)

### 4. Start Chat Frontend
```bash
# Terminal 2
./start-chat-frontend.sh

# Should see:
# "Starting Chat Frontend..."
# "ready - started server on 0.0.0.0:3001"
```

- [ ] Frontend running
- [ ] Can access http://localhost:3001
- [ ] Welcome screen displays

## 🧪 Quick Test

### Test 1: Create Session
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test123", "mode": "onboarding"}'
```

- [ ] Returns JSON with `session_id`
- [ ] No errors

### Test 2: Frontend Flow
1. Open http://localhost:3001
2. Enter user ID: `test123`
3. Click "Start with Assessment"
4. Should see chat interface
5. Type `start` and press Enter
6. Should receive response from OnboardingAgent

- [ ] Welcome screen loads
- [ ] Can create session
- [ ] Chat interface displays
- [ ] Can send messages
- [ ] Receives responses
- [ ] Typing indicator works

### Test 3: WebSocket Connection
In browser console (http://localhost:3001):
```javascript
// After creating a session, check WebSocket connection
// Should see green "Connected" indicator in header
```

- [ ] Connection status shows "Connected"
- [ ] Messages send/receive in real-time
- [ ] No WebSocket errors in console

## 🐛 Troubleshooting

### API Server Won't Start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# If needed, kill the process
kill -9 <PID>

# Try starting again
./start-api-server.sh
```

### Frontend Won't Start
```bash
cd chat_frontend

# Clear cache
rm -rf .next node_modules

# Reinstall
npm install

# Try again
npm run dev
```

### WebSocket Connection Fails
- [ ] Check API server is running (Terminal 1)
- [ ] Verify session was created successfully
- [ ] Check browser console for errors
- [ ] Try refreshing the page

### AWS Bedrock Errors
```bash
# Verify credentials
aws sts get-caller-identity

# Check region
echo $AWS_DEFAULT_REGION
```

- [ ] Credentials valid
- [ ] Region is `us-east-1`
- [ ] Bedrock access enabled in IAM

## 📚 Next Steps

Once everything is working:

- [ ] Read [CHAT_INTERFACE_README.md](./CHAT_INTERFACE_README.md) for full guide
- [ ] Explore API docs at http://localhost:8000/docs
- [ ] Test different user flows (new user, returning user)
- [ ] Try onboarding quiz with different questions
- [ ] Review code in `api_server/` and `chat_frontend/`

## 🎯 Expected Results

After completing all steps:

✅ **API Server**: Running on http://localhost:8000
✅ **Frontend**: Running on http://localhost:3001
✅ **WebSocket**: Connected (green indicator)
✅ **Onboarding**: Can start and complete quiz
✅ **Chat Mode**: Can chat after onboarding complete

## 📝 File Structure Check

Verify these files exist:

```bash
# API Server
ls -la api_server/main.py
ls -la api_server/requirements.txt

# Frontend
ls -la chat_frontend/package.json
ls -la chat_frontend/src/app/page.tsx

# Scripts
ls -la setup_chat_interface.sh
ls -la start-api-server.sh
ls -la start-chat-frontend.sh

# Agents
ls -la agents/onboarding/agent.py
ls -la agents/onboarding/tools.py
ls -la shared/models.py
```

- [ ] All files exist
- [ ] Scripts are executable (`-rwxr-xr-x`)

## 🔄 Common Commands

```bash
# Check what's running on ports
lsof -i :8000  # API server
lsof -i :3001  # Frontend

# View API logs
# (Terminal 1 where API is running)

# View frontend logs
# (Terminal 2 where frontend is running)

# Test API health
curl http://localhost:8000/

# Test session creation
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "myuser", "mode": "orchestrator"}'
```

## ✨ Success!

If all checks pass:

🎉 **Your chat interface is ready to use!**

Open http://localhost:3001 and start chatting with your Learning Assistant!

---

**Need help?** Check:
- [CHAT_INTERFACE_README.md](./CHAT_INTERFACE_README.md) - Detailed documentation
- [COMPLETE_SYSTEM_README.md](./COMPLETE_SYSTEM_README.md) - Full system guide
- [IMPLEMENTATION_COMPLETE.md](./IMPLEMENTATION_COMPLETE.md) - Implementation summary
- API Docs: http://localhost:8000/docs
