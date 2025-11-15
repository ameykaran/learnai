"""Tool wrappers for specialist agents.

Wrappers try to use `strands` if available and otherwise provide safe stubs
so other modules can import these wrappers without failing.
"""
from typing import Any, Callable
import logging
import time
import json

# Try to import strands; fall back to stubs if not available.
try:
    from strands import Agent  # type: ignore
    from strands.tools import tool  # type: ignore
except Exception:
    Agent = None  # type: ignore

    def tool(fn: Callable) -> Callable:
        # no-op decorator when strands.tools.tool isn't available
        return fn

# Try to import specialist math agent
try:
    from .specialist_math_agent import get_specialist_math_agent
    _MATH_AGENT_AVAILABLE = True
except Exception as e:
    _MATH_AGENT_AVAILABLE = False
    logging.getLogger(__name__).warning("Specialist math agent not available: %s", e)

log = logging.getLogger(__name__)


class AgentStub:
    """Minimal agent stub used when real Agent is not available.

    It simply echoes a canned response indicating which agent was called.
    """

    def __init__(self, name: str):
        self.name = name

    def __call__(self, prompt: str, *args, **kwargs) -> str:
        log.debug("AgentStub %s called", self.name)
        return f"[Stubbed {self.name} agent response] Prompt summary: {str(prompt)[:240]}"


# instantiate agent objects (real or stub)
if Agent is not None:
    try:
        retriever_agent = Agent(name="content_retriever")
        content_gen_agent = Agent(name="content_generator")
        quiz_agent = Agent(name="quiz_agent")
        report_agent = Agent(name="report_agent")
        specialist_agent = Agent(name="specialist_agent")
    except Exception:
        retriever_agent = AgentStub("content_retriever")
        content_gen_agent = AgentStub("content_generator")
        quiz_agent = AgentStub("quiz_agent")
        report_agent = AgentStub("report_agent")
        specialist_agent = AgentStub("specialist_agent")
else:
    retriever_agent = AgentStub("content_retriever")
    content_gen_agent = AgentStub("content_generator")
    quiz_agent = AgentStub("quiz_agent")
    report_agent = AgentStub("report_agent")
    specialist_agent = AgentStub("specialist_agent")


def _run_agent(agent: Any, prompt: str, *args, **kwargs) -> str:
    """Uniform runner for real Agent or stub.

    Logs input, output and timing so each call is auditable.
    Converts AgentResult objects to strings.
    """
    start = time.time()
    log.debug("Agent call start: %s", getattr(agent, "name", str(agent)))
    log.debug("Agent input (truncated): %s", str(prompt)[:500])
    try:
        out = agent(prompt, *args, **kwargs)
        
        # Convert AgentResult to string if needed
        if hasattr(out, 'content'):
            # Strands AgentResult object
            out_str = str(out.content)
        elif hasattr(out, 'text'):
            # Alternative format
            out_str = str(out.text)
        else:
            # Already a string or other type
            out_str = str(out)
        
        duration = (time.time() - start) * 1000.0
        # structured log entry
        log.info(
            "agent_call",
            extra={
                "extra_json": {
                    "agent": getattr(agent, "name", str(agent)),
                    "input_summary": str(prompt)[:500],
                    "output_summary": out_str[:1000],
                    "duration_ms": int(duration),
                }
            },
        )
        return out_str
    except Exception as e:
        duration = (time.time() - start) * 1000.0
        log.exception("Agent execution failed: %s", e)
        log.info(
            "agent_call_error",
            extra={
                "extra_json": {
                    "agent": getattr(agent, "name", str(agent)),
                    "error": str(e),
                    "duration_ms": int(duration),
                }
            },
        )
        return f"[agent-error] {e}"


@tool
def content_retriever_tool(query: str, context: str = "") -> str:
    """Retrieve relevant documents for `query`.

    In production this should call your RAG/vector DB tools. Here we call
    the retriever_agent (real or stub).
    """
    prompt = f"Retrieve context for query:\n{query}\nExisting context:\n{context}"
    return _run_agent(retriever_agent, prompt)


@tool
def content_generator_tool(query: str, retrieved_docs: str) -> str:
    prompt = f"Create teaching content. Query:\n{query}\n\nContext:\n{retrieved_docs}"
    return _run_agent(content_gen_agent, prompt)


@tool
def quiz_agent_tool(query: str, retrieved_docs: str, difficulty: str = "medium") -> str:
    prompt = (
        f"Generate quiz for: {query}\nDifficulty: {difficulty}\nContext:\n{retrieved_docs}"
    )
    return _run_agent(quiz_agent, prompt)


@tool
def report_agent_tool(user_id: str, time_period: str = "all") -> str:
    prompt = f"Generate performance report for user: {user_id}\nTime period: {time_period}"
    return _run_agent(report_agent, prompt)


@tool
def specialist_agent_tool(query: str, retrieved_docs: str) -> str:
    """Specialist tool for domain-specific problem solving.
    
    If domain is 'math' and the math agent is available, uses the finetuned
    LiquidAI math model. Otherwise falls back to generic specialist agent.
    """
    # Use specialized math agent for math domain
    if _MATH_AGENT_AVAILABLE:
        try:
            math_agent = get_specialist_math_agent()
            return _run_agent(math_agent, query, retrieved_docs=retrieved_docs)
        except Exception as e:
            log.exception("Math agent failed, falling back to generic: %s", e)
    
    # Fallback to generic specialist agent
    prompt = f"Query: {query}\nContext:\n{retrieved_docs}"
    return _run_agent(specialist_agent, prompt)


__all__ = [
    "content_retriever_tool",
    "content_generator_tool",
    "quiz_agent_tool",
    "report_agent_tool",
    "specialist_agent_tool",
]
