"""
API Server for Learning Management System
Provides REST and WebSocket endpoints for chat interface
"""

from fastapi import FastAPI, WebSocket, HTTPException, Depends, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
import json
from datetime import datetime
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.onboarding import OnboardingAgent
from shared.models import UserProfile
from logging_config import configure_logging, get_logger
import os

# Configure logging to suppress verbose warnings
# Set DEBUG_MODE=true in environment for detailed debugging
# configure_logging()
logger = get_logger(__name__)

logger.info("=" * 70)
logger.info("  Initializing API Server")
# logger.info(f"  Debug Mode: {DEBUG_MODE}")
logger.info(f"  AWS Region: {os.getenv('AWS_DEFAULT_REGION', os.getenv('AWS_REGION', 'us-east-1'))}")
logger.info(f"  AWS Access Key: {'✓ Set' if os.getenv('AWS_ACCESS_KEY_ID') else '✗ NOT SET'}")
logger.info(f"  AWS Secret Key: {'✓ Set' if os.getenv('AWS_SECRET_ACCESS_KEY') else '✗ NOT SET'}")
logger.info("=" * 70)

from fastapi import FastAPI, WebSocket, HTTPException, Depends, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
import json
from datetime import datetime
import asyncio
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.onboarding import OnboardingAgent
from shared.models import UserProfile


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- STARTUP ----
    print("=" * 70)
    print("  Learning Management API Server Starting")
    print("=" * 70)
    print(f"  REST API: http://localhost:8000")
    print(f"  WebSocket: ws://localhost:8000/ws/{{session_id}}")
    print(f"  Docs: http://localhost:8000/docs")
    print("=" * 70)

    yield  # ---- APPLICATION RUNNING ----

    # ---- SHUTDOWN ----
    print("\nShutting down API server...")

app = FastAPI(
    title="Learning Management API",
    description="API for orchestrator and agent chat interface",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

class SessionManager:
    """Manages user sessions and conversation history."""
    
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.user_profiles: Dict[str, UserProfile] = {}
    
    def create_session(self, user_id: str) -> str:
        """Create a new session for a user."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user_id,
            "session_id": session_id,
            "created_at": datetime.now(),
            "mode": "orchestrator",  # or "direct_agent"
            "current_agent": None,
            "conversation_history": [],
            "agent_state": {}
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data."""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, updates: dict):
        """Update session data."""
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to conversation history."""
        if session_id in self.sessions:
            self.sessions[session_id]["conversation_history"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
    
    def store_profile(self, user_id: str, profile: UserProfile):
        """Store user profile in memory."""
        self.user_profiles[user_id] = profile
        logger.info(f"💾 Profile stored for user {user_id}: {profile.competence_level} level")
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile."""
        return self.user_profiles.get(user_id)
    
    def has_profile(self, user_id: str) -> bool:
        """Check if user has a profile."""
        return user_id in self.user_profiles
    
    def get_all_profiles(self) -> Dict[str, UserProfile]:
        """Get all stored profiles (for orchestrator/agent use)."""
        return self.user_profiles.copy()

# Global session manager
session_manager = SessionManager()

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateSessionRequest(BaseModel):
    user_id: str
    mode: str = "orchestrator"  # "orchestrator" or "onboarding"

class CreateSessionResponse(BaseModel):
    session_id: str
    user_id: str
    mode: str
    message: str

class ChatMessage(BaseModel):
    session_id: str
    message: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    agent: Optional[str] = None
    mode: str
    metadata: Optional[dict] = None

class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    mode: str
    current_agent: Optional[str]
    message_count: int
    has_profile: bool

# ============================================================================
# WEBSOCKET CONNECTION MANAGER
# ============================================================================

class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, session_id: str, websocket: WebSocket):
        """Accept and store WebSocket connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: dict):
        """Send message to specific session."""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)
    
    async def send_text(self, session_id: str, text: str):
        """Send text message to specific session."""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(text)

websocket_manager = ConnectionManager()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Learning Management API",
        "status": "running",
        "version": "1.0.0"
    }

@app.post("/api/sessions", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    """
    Create a new chat session.
    
    Modes:
    - "orchestrator": General chat with orchestrator (default)
    - "onboarding": Direct connection to onboarding agent
    """
    session_id = session_manager.create_session(request.user_id)
    session_manager.update_session(session_id, {"mode": request.mode})
    
    # Check if user has profile
    profile = session_manager.get_profile(request.user_id)
    
    if request.mode == "onboarding" and profile:
        return CreateSessionResponse(
            session_id=session_id,
            user_id=request.user_id,
            mode="orchestrator",  # Switch to orchestrator
            message="You have already completed onboarding. Switching to general chat mode."
        )
    
    return CreateSessionResponse(
        session_id=session_id,
        user_id=request.user_id,
        mode=request.mode,
        message=f"Session created in {request.mode} mode"
    )

@app.get("/api/sessions/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """Get information about a session."""
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    user_id = session["user_id"]
    profile = session_manager.get_profile(user_id)
    
    return SessionInfo(
        session_id=session_id,
        user_id=user_id,
        mode=session["mode"],
        current_agent=session.get("current_agent"),
        message_count=len(session["conversation_history"]),
        has_profile=profile is not None
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Send a chat message.
    
    Routes to orchestrator or direct agent based on session mode.
    """
    session = session_manager.get_session(message.session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Add user message to history
    session_manager.add_message(message.session_id, "user", message.message)
    
    mode = session["mode"]
    user_id = session["user_id"]
    
    try:
        if mode == "onboarding":
            # Direct connection to onboarding agent
            response_text, metadata = await handle_onboarding(
                user_id=user_id,
                session_id=message.session_id,
                message=message.message,
                session=session
            )
            agent_name = "OnboardingAgent"
            
        else:
            # Route through orchestrator
            response_text, metadata = await handle_orchestrator(
                user_id=user_id,
                message=message.message,
                session=session
            )
            agent_name = "Orchestrator"
        
        # Add assistant response to history
        session_manager.add_message(message.session_id, "assistant", response_text)
        
        return ChatResponse(
            session_id=message.session_id,
            response=response_text,
            agent=agent_name,
            mode=mode,
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/api/sessions/{session_id}/history")
async def get_conversation_history(session_id: str):
    """Get conversation history for a session."""
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "history": session["conversation_history"]
    }

@app.get("/api/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile if exists."""
    profile = session_manager.get_profile(user_id)
    
    if not profile:
        return {
            "user_id": user_id,
            "has_profile": False,
            "message": "User has not completed onboarding"
        }
    
    return {
        "user_id": user_id,
        "has_profile": True,
        "profile": profile.to_dict()
    }

# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat.
    
    Supports streaming responses from agents.
    """
    logger.info(f"🔌 WebSocket connection attempt for session: {session_id}")
    
    session = session_manager.get_session(session_id)
    
    if not session:
        logger.warning(f"❌ WebSocket rejected - session not found: {session_id}")
        await websocket.close(code=1008, reason="Session not found")
        return
    
    await websocket_manager.connect(session_id, websocket)
    logger.info(f"✅ WebSocket connected for session: {session_id} (mode: {session['mode']})")
    
    try:
        # Send welcome message
        await websocket_manager.send_message(session_id, {
            "type": "connected",
            "session_id": session_id,
            "mode": session["mode"]
        })
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_text = message_data.get("message", "")
            
            # Add to history
            session_manager.add_message(session_id, "user", message_text)
            
            # Send typing indicator
            await websocket_manager.send_message(session_id, {
                "type": "typing",
                "agent": session["mode"]
            })
            
            # Process message based on mode
            mode = session["mode"]
            user_id = session["user_id"]
            
            try:
                if mode == "onboarding":
                    response_text, metadata = await handle_onboarding(
                        user_id=user_id,
                        session_id=session_id,
                        message=message_text,
                        session=session,
                        websocket_manager=websocket_manager  # Pass WebSocket manager for streaming
                    )
                else:
                    response_text, metadata = await handle_orchestrator(
                        user_id=user_id,
                        message=message_text,
                        session=session
                    )
                
                # Add to history (only if response is not empty)
                if response_text and response_text.strip():
                    session_manager.add_message(session_id, "assistant", response_text)
                
                # Send response (only if response is not empty)
                if response_text and response_text.strip():
                    await websocket_manager.send_message(session_id, {
                        "type": "message",
                        "role": "assistant",
                        "content": response_text,
                        "metadata": metadata
                    })
                elif metadata.get("tools_sent_messages"):
                    logger.info("ℹ️  Tools sent messages directly, skipping final response")
                    # Send a done signal to clear typing indicator
                    await websocket_manager.send_message(session_id, {
                        "type": "done",
                        "metadata": metadata
                    })
                
            except Exception as e:
                await websocket_manager.send_message(session_id, {
                    "type": "error",
                    "message": f"Error: {str(e)}"
                })
    
    except WebSocketDisconnect:
        logger.info(f"🔌 WebSocket disconnected normally: {session_id}")
        websocket_manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"❌ WebSocket error for session {session_id}: {e}")
        websocket_manager.disconnect(session_id)

# ============================================================================
# AGENT HANDLERS
# ============================================================================

async def handle_onboarding(
    user_id: str, 
    session_id: str, 
    message: str, 
    session: dict,
    websocket_manager: Optional['ConnectionManager'] = None
) -> tuple:
    """
    Handle onboarding agent interaction.
    
    Direct connection to onboarding agent for quiz flow.
    Sends intermediate messages for each tool call if WebSocket is available.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"🔵 handle_onboarding called:")
    logger.info(f"   user_id: {user_id}")
    logger.info(f"   session_id: {session_id}")
    logger.info(f"   message: {message[:50]}...")
    
    # Get or create onboarding agent for this session
    agent_state = session.get("agent_state", {})
    
    if "onboarding_agent" not in agent_state:
        logger.info("📝 Creating new OnboardingAgent instance...")
        try:
            agent = OnboardingAgent()
            logger.info("✅ OnboardingAgent created successfully")
            
            # Set up profile callback to automatically store profiles
            def profile_callback(uid: str, profile: UserProfile):
                logger.info(f"📥 Profile callback triggered for user {uid}")
                session_manager.store_profile(uid, profile)
                logger.info(f"✅ Profile stored in orchestrator memory: {profile.competence_level} level")
            
            agent.tools_instance.set_profile_callback(profile_callback)
            logger.info("🔗 Profile callback registered")
            
            agent_state["onboarding_agent"] = agent
            agent_state["quiz_started"] = False
            session_manager.update_session(session_id, {"agent_state": agent_state})
        except Exception as e:
            logger.error(f"❌ Failed to create OnboardingAgent: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize agent: {str(e)}")
    else:
        logger.info("♻️  Reusing existing OnboardingAgent instance")
    
    agent = agent_state["onboarding_agent"]
    
    # Set up tool callback to send intermediate messages
    # This must be done before each chat call to ensure it's registered
    if websocket_manager:
        async def send_tool_message(msg: str):
            """Send tool output as separate WebSocket message."""
            try:
                # Turn off typing indicator before showing tool message
                await websocket_manager.send_message(session_id, {
                    "type": "typing_off"
                })
                
                # Send the tool message
                await websocket_manager.send_message(session_id, {
                    "type": "tool_message",
                    "role": "assistant",
                    "content": msg,
                    "metadata": {"source": "tool_output", "timestamp": datetime.now().isoformat()}
                })
                logger.info(f"📤 Sent tool message via WebSocket ({len(msg)} chars)")
                
                # Brief pause for readability
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Failed to send tool message: {e}")
        
        # Register the async callback
        agent.tools_instance.set_websocket_callback(send_tool_message)
        logger.info("🔗 WebSocket callback registered for tool messages")
    
    # Check if this is the start
    if not agent_state.get("quiz_started"):
        agent_state["quiz_started"] = True
        session_manager.update_session(session_id, {"agent_state": agent_state})

        # Send the initial prompt to start the quiz
        response = agent.assess_user(user_id=user_id, total_questions=session.get("total_questions"))
        logger.info("🎬 Quiz session started")
        metadata = {
            "agent": "OnboardingAgent",
            "quiz_active": True,
            "profile_complete": False
        }
        return response, metadata

    # Send message to agent
    try:
        logger.info(f"📤 Sending message to agent: {message[:50]}...")
        response = await agent.chat_async(message, user_id=user_id)
        logger.info(f"📥 Received response from agent ({len(str(response))} chars)")
    except Exception as e:
        logger.error(f"❌ Error calling agent.chat_async(): {e}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
    
    # Check if profile was generated
    # The callback should have automatically stored it if finalize_assessment was called
    profile = session_manager.get_profile(user_id)
    
    if not profile:
        # Also check the tools instance directly in case callback didn't trigger
        last_profile = agent.tools_instance.get_last_profile()
        if last_profile and last_profile.user_id == user_id:
            session_manager.store_profile(user_id, last_profile)
            profile = last_profile
            logger.info(f"✅ Profile retrieved from tools and stored: {profile.competence_level} level")
    
    if not profile:
        logger.info("ℹ️  No profile found yet (quiz in progress)")
    else:
        logger.info(f"✅ Profile available: {profile.competence_level} level")
    
    metadata = {
        "agent": "OnboardingAgent",
        "quiz_active": True,
        "profile_complete": profile is not None,
        "tools_sent_messages": websocket_manager is not None  # Flag that tools already sent output
    }
    
    # If profile complete, switch mode
    if profile:
        session_manager.update_session(session_id, {"mode": "orchestrator"})
        metadata["mode_switched"] = True
        metadata["message"] = "Onboarding complete! Switching to general chat."
        logger.info("🎉 Onboarding complete! Switching to orchestrator mode")
    
    # If tools sent messages via WebSocket, return minimal response
    # Otherwise return the full agent response
    if websocket_manager:
        return "", metadata  # Empty response since tools already sent everything
    else:
        return response, metadata

async def handle_orchestrator(user_id: str, message: str, session: dict) -> tuple:
    """
    Handle orchestrator interaction.
    
    Routes message through orchestrator which delegates to appropriate agents.
    Other agents can access user profile from session_manager for personalization.
    """
    # Check if user has profile
    profile = session_manager.get_profile(user_id)
    
    if not profile:
        # User needs onboarding first
        return (
            "👋 Welcome! I see you haven't completed your onboarding assessment yet. "
            "This helps me understand your current knowledge level so I can personalize your learning experience. "
            "Would you like to start the assessment now?",
            {
                "agent": "Orchestrator",
                "action_required": "onboarding",
                "message": "User needs onboarding"
            }
        )
    
    # TODO: Implement actual orchestrator agent
    # For now, return a placeholder showing profile access
    response = f"[Orchestrator processing message: {message}]\n\n"
    response += f"📊 Your Learning Profile:\n"
    response += f"  • Competence Level: {profile.competence_level}\n"
    response += f"  • Ability Score: {profile.ability_score:.2f}\n"
    response += f"  • Overall Accuracy: {profile.overall_accuracy:.1f}%\n"
    response += f"  • Recommended Starting Level: {profile.recommended_starting_level}\n"
    response += f"  • Learning Pace: {profile.learning_pace}\n\n"
    
    if profile.strengths:
        response += f"💪 Strengths: {', '.join(profile.strengths)}\n"
    if profile.weaknesses:
        response += f"📚 Areas for Improvement: {', '.join(profile.weaknesses)}\n\n"
    
    response += "ℹ️ This profile is now available to all agents for personalized learning!"
    
    metadata = {
        "agent": "Orchestrator",
        "user_competence": profile.competence_level,
        "ability_score": profile.ability_score,
        "recommended_level": profile.recommended_starting_level,
        "profile_available": True
    }
    
    return response, metadata

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
