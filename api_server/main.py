"""
API Server for Learning Management System
Provides REST and WebSocket endpoints for orchestrator + onboarding agents.
"""

# ============================================================================
# IMPORTS
# ============================================================================

from api_server.logging_config import get_logger
from agents.retrieval.backend.rag_system import RAGSystem
from shared.models import UserProfile
from agents.content_generation.agent import (
    generate_pdf_document,
    generate_presentation_slides,
)
from agents.orchestrator.adapter import create_content_generation_request
from agents.orchestrator.orchestrator import create_workflow_orchestrator
from api_server.orchestrator_handler import handle_workflow_orchestrator
from agents.onboarding import OnboardingAgent
import sys
import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional, Dict

from fastapi import (
    FastAPI,
    WebSocket,
    HTTPException,
    WebSocketDisconnect
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Project imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


logger = get_logger(__name__)


# ============================================================================
# GLOBAL STATE
# ============================================================================

orchestrator_agent = None
rag_system = None
PUBLIC_DIR = Path(__file__).parent / "public"
PUBLIC_DIR.mkdir(exist_ok=True)


# ============================================================================
# LIFESPAN (Startup / Shutdown)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator_agent, rag_system

    print("=" * 70)
    print("  Learning Management API Server Starting")
    print("=" * 70)
    print("REST API:       http://localhost:8000")
    print("WebSocket:      ws://localhost:8000/ws/<session_id>")
    print("Docs:           http://localhost:8000/docs")
    print("=" * 70)

    # Initialize RAG
    try:
        print("📚 Initializing RAG system...")
        rag_system = RAGSystem()
        print("✅ RAG initialized")
    except Exception as exc:
        print(f"⚠️ RAG init failed: {exc}")
        rag_system = None

    # Initialize Workflow Orchestrator
    try:
        print("🤖 Initializing Workflow Orchestrator...")
        orchestrator_agent = create_workflow_orchestrator(rag_system=rag_system)
        print("✅ Workflow Orchestrator ready")
        print(f"   - Registered agents: {list(orchestrator_agent.agents.keys())}")
        print(f"   - Query types: {list(orchestrator_agent.classifier.query_types.keys())}")
    except Exception as exc:
        print(f"⚠️ Orchestrator init failed: {exc}")
        orchestrator_agent = None

    yield

    print("Shutting down server...")



# ============================================================================
# FASTAPI INSTANCE
# ============================================================================

app = FastAPI(
    title="Learning Management API",
    version="1.0.0",
    description="REST & WebSocket API providing orchestrator + agent chat",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files
app.mount("/generated", StaticFiles(directory=str(PUBLIC_DIR)), name="generated")


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

class SessionManager:
    """Manages user sessions and conversation history."""

    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.user_profiles: Dict[str, UserProfile] = {}

    def create_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "mode": "orchestrator",
            "current_agent": None,
            "conversation_history": [],
            "agent_state": {}
        }
        return session_id

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)

    def update_session(self, session_id: str, updates: dict):
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)

    def add_message(self, session_id: str, role: str, content: str):
        if session_id in self.sessions:
            self.sessions[session_id]["conversation_history"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })

    # Profile Management
    def store_profile(self, user_id: str, profile: UserProfile):
        self.user_profiles[user_id] = profile
        logger.info(f"Profile stored for user {user_id}")

    def get_profile(self, user_id: str):
        return self.user_profiles.get(user_id)


session_manager = SessionManager()


# ============================================================================
# MODELS
# ============================================================================

class CreateSessionRequest(BaseModel):
    user_id: str
    mode: str = "orchestrator"


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
    agent: str
    mode: str
    metadata: Optional[dict]


class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    mode: str
    current_agent: Optional[str]
    message_count: int
    has_profile: bool


class GenerateContentRequest(BaseModel):
    user_id: str
    topic: str
    request_type: str  # pdf | slides
    num_slides: Optional[int] = 10
    include_exercises: bool = False


class GenerateContentResponse(BaseModel):
    success: bool
    topic: str
    request_type: str
    file_url: Optional[str] = None
    filename: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None


# ============================================================================
# WEBSOCKET CONNECTION MANAGER
# ============================================================================

class ConnectionManager:
    """Tracks active WebSocket connections."""

    def __init__(self):
        self.active: Dict[str, WebSocket] = {}

    async def connect(self, session_id: str, ws: WebSocket):
        await ws.accept()
        self.active[session_id] = ws

    def disconnect(self, session_id: str):
        self.active.pop(session_id, None)

    async def send_json(self, session_id: str, payload: dict):
        if session_id in self.active:
            await self.active[session_id].send_json(payload)


ws_manager = ConnectionManager()


# ============================================================================
# ROUTES - BASIC
# ============================================================================

@app.get("/")
async def root():
    return {"status": "running", "service": "Learning Management API"}


# ============================================================================
# SESSION ROUTES
# ============================================================================

@app.post("/api/sessions", response_model=CreateSessionResponse)
async def create_session(req: CreateSessionRequest):
    session_id = session_manager.create_session(req.user_id)
    session_manager.update_session(session_id, {"mode": req.mode})

    profile_exists = session_manager.get_profile(req.user_id)

    # Prevent redundant onboarding
    if req.mode == "onboarding" and profile_exists:
        return CreateSessionResponse(
            session_id=session_id,
            user_id=req.user_id,
            mode="orchestrator",
            message="User already onboarded, switched to orchestrator."
        )

    return CreateSessionResponse(
        session_id=session_id,
        user_id=req.user_id,
        mode=req.mode,
        message=f"Session created in {req.mode} mode"
    )


@app.get("/api/sessions/{session_id}", response_model=SessionInfo)
async def session_info(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    profile = session_manager.get_profile(session["user_id"])

    return SessionInfo(
        session_id=session_id,
        user_id=session["user_id"],
        mode=session["mode"],
        current_agent=session.get("current_agent"),
        message_count=len(session["conversation_history"]),
        has_profile=profile is not None,
    )


@app.get("/api/sessions/{session_id}/history")
async def conversation_history(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session["conversation_history"]


# ============================================================================
# CHAT ROUTE
# ============================================================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatMessage):
    session = session_manager.get_session(req.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    session_manager.add_message(req.session_id, "user", req.message)
    mode = session["mode"]
    user_id = session["user_id"]

    if mode == "onboarding":
        response, meta = await handle_onboarding(user_id, req.session_id, req.message, session)
        agent = "OnboardingAgent"
    else:
        response, meta = await handle_orchestrator(user_id, req.message, session)
        agent = "Orchestrator"

    session_manager.add_message(req.session_id, "assistant", response)

    return ChatResponse(
        session_id=req.session_id,
        response=response,
        agent=agent,
        mode=mode,
        metadata=meta,
    )


# ============================================================================
# PROFILE ROUTE
# ============================================================================

@app.get("/api/users/{user_id}/profile")
async def get_profile(user_id: str):
    profile = session_manager.get_profile(user_id)
    if not profile:
        return {"user_id": user_id, "has_profile": False}
    return {"user_id": user_id, "has_profile": True, "profile": profile.to_dict()}


# ============================================================================
# CONTENT GENERATION ROUTE
# ============================================================================

@app.post("/api/generate", response_model=GenerateContentResponse)
async def generate(req: GenerateContentRequest):
    profile = session_manager.get_profile(req.user_id)
    if not profile:
        return GenerateContentResponse(
            success=False,
            topic=req.topic,
            request_type=req.request_type,
            error="User must complete onboarding before generating content."
        )

    try:
        rag_chunks = []
        if rag_system:
            try:
                rag_chunks = [
                    c.to_dict() if hasattr(c, "to_dict") else c
                    for c in rag_system.query(req.topic, k=10)
                ]
            except Exception as exc:
                logger.warning(f"RAG query failed: {exc}")

        agent_req = create_content_generation_request(
            topic=req.topic,
            request_type=req.request_type,
            rag_chunks=rag_chunks,
            user_profile=profile,
            num_slides=req.num_slides,
            include_exercises=req.include_exercises,
        )

        markdown = f"""---
title: {req.topic}
author: {req.user_id}
date: {datetime.now().date()}
---
{agent_req['prompt']}
"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_hash = hashlib.md5(req.topic.encode()).hexdigest()[:8]
        filename = f"{req.request_type}_{topic_hash}_{timestamp}.pdf"
        output_path = PUBLIC_DIR / filename

        if req.request_type == "slides":
            generate_presentation_slides(markdown, str(output_path))
        else:
            generate_pdf_document(markdown, str(output_path), title=req.topic)

        file_url = f"/generated/{filename}"

        return GenerateContentResponse(
            success=True,
            topic=req.topic,
            request_type=req.request_type,
            filename=filename,
            file_url=file_url,
            metadata={
                "chunks_used": len(rag_chunks),
                "level": profile.competence_level,
            }
        )

    except Exception as exc:
        logger.error(f"Content generation error: {exc}")
        return GenerateContentResponse(
            success=False,
            topic=req.topic,
            request_type=req.request_type,
            error=str(exc)
        )


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws/{session_id}")
async def ws_endpoint(ws: WebSocket, session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        await ws.close(code=1008, reason="Session not found")
        return

    await ws_manager.connect(session_id, ws)

    try:
        await ws_manager.send_json(session_id, {
            "type": "connected",
            "session_id": session_id,
            "mode": session["mode"],
        })

        while True:
            payload = await ws.receive_text()
            data = json.loads(payload)
            user_msg = data.get("message", "")

            session_manager.add_message(session_id, "user", user_msg)

            mode = session["mode"]
            user_id = session["user_id"]

            if mode == "onboarding":
                resp, meta = await handle_onboarding(user_id, session_id, user_msg, session)
            else:
                resp, meta = await handle_orchestrator(user_id, user_msg, session)

            session_manager.add_message(session_id, "assistant", resp)

            await ws_manager.send_json(session_id, {
                "type": "message",
                "role": "assistant",
                "content": resp,
                "metadata": meta
            })

    except WebSocketDisconnect:
        ws_manager.disconnect(session_id)


# ============================================================================
# AGENT HANDLERS
# ============================================================================

async def handle_onboarding(user_id: str, session_id: str, message: str, session: dict):
    """Wrapper around OnboardingAgent with auto-profile storage."""
    state = session["agent_state"]

    if "agent" not in state:
        agent = OnboardingAgent()

        def profile_callback(uid: str, profile: UserProfile):
            session_manager.store_profile(uid, profile)

        agent.tools_instance.set_profile_callback(profile_callback)

        state["agent"] = agent
        state["started"] = False

        session_manager.update_session(session_id, {"agent_state": state})

    agent = state["agent"]

    # Start onboarding flow
    if not state["started"]:
        state["started"] = True
        session_manager.update_session(session_id, {"agent_state": state})

        resp = agent.assess_user(user_id=user_id)
        return resp, {"agent": "OnboardingAgent", "quiz_active": True}

    # Continue quiz
    resp = await agent.chat_async(message, user_id=user_id)
    profile = session_manager.get_profile(user_id)

    meta = {
        "agent": "OnboardingAgent",
        "quiz_active": profile is None,
        "profile_complete": profile is not None
    }

    # Auto-switch to orchestrator
    if profile:
        session_manager.update_session(session_id, {"mode": "orchestrator"})
        meta["mode_switched"] = True

    return resp, meta


async def handle_orchestrator(user_id: str, message: str, session: dict):
    # """Process messages via Orchestrator unless onboarding required."""
    # profile = session_manager.get_profile(user_id)

    # if not profile:
    #     return (
    #         "You must complete onboarding first. Shall I start the assessment?",
    #         {"agent": "Orchestrator", "needs_onboarding": True}
    #     )

    # if orchestrator_agent is None:
    #     return (
    #         "Orchestrator not available. Showing profile only.",
    #         {"fallback": True}
    #     )

    # try:
    #     # Ensure profile loaded into orchestrator memory
    #     orchestrator_agent.user_profiles.setdefault(user_id, profile)

    #     resp = orchestrator_agent.chat(message, user_id=user_id)
    #     return resp, {"agent": "Orchestrator"}

    # except Exception as exc:
    #     logger.error(f"Orchestrator error: {exc}")
    #     return "Error in orchestrator.", {"error": str(exc)}
    return await handle_workflow_orchestrator(
        user_id=user_id,
        message=message,
        session=session,
        orchestrator=orchestrator_agent,
        session_manager=session_manager
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
