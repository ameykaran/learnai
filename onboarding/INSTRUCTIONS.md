# 🚀 How to Run the Adaptive Probability Quiz

## ✅ FIXED ISSUES:
- ✅ CORS configuration updated to allow port 3001
- ✅ Frontend components created and properly configured
- ✅ Backend API endpoints tested and working
- ✅ Database populated with 73+ probability questions

## 📋 SIMPLE STARTUP INSTRUCTIONS:

### Option 1: Use the Automated Scripts (RECOMMENDED)

**Terminal 1 - Start Backend:**
```bash
cd /home/sree/random/agentSME/chunker/majorprojectfull/lma-major-project-moya-moye/onboarding
./start-backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
cd /home/sree/random/agentSME/chunker/majorprojectfull/lma-major-project-moya-moye/onboarding
./start-frontend.sh
```

### Option 2: Manual Commands

**Terminal 1 - Backend:**
```bash
cd /home/sree/random/agentSME/chunker/majorprojectfull/lma-major-project-moya-moye/onboarding/backend
python3 main.py
```

**Terminal 2 - Frontend:**
```bash
cd /home/sree/random/agentSME/chunker/majorprojectfull/lma-major-project-moya-moye/onboarding/frontend
npm run dev
```

## 🎯 EXPECTED BEHAVIOR:

1. **Backend should show:**
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   ```

2. **Frontend should show:**
   ```
   ▲ Next.js 14.0.4
   - Local:        http://localhost:3000   (or http://localhost:3001)
   ✓ Ready in X.Xs
   ```

3. **Open Browser:** http://localhost:3000 or http://localhost:3001

4. **You Should See:**
   - Beautiful blue gradient background
   - "Probability Quiz" title
   - "How it works" section with steps 1-3
   - Working "Start Quiz" button (no more errors!)

## 🔧 WHAT WAS FIXED:

- **CORS Issue:** Added `http://localhost:3001` to allowed origins
- **Component Structure:** All React components created in correct locations
- **Styling:** Tailwind CSS properly configured for version 3.x
- **Font Issues:** Replaced Geist fonts with Inter (compatible)
- **API Endpoints:** All backend endpoints tested and working

## 🎮 TESTING THE QUIZ:

1. Click "Start Quiz"
2. Answer questions (starts with easy, adapts based on performance)
3. Complete 25 questions
4. See your competence level: Easy/Medium/Difficult
5. View detailed performance breakdown
6. Option to retake the quiz

The application is now fully functional with the CORS issue resolved!