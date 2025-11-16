"""Deterministic orchestrator that enforces workflow rules and routes to agents.

This module implements a DeterministicOrchestrator that:
- classifies incoming queries
- always runs the retriever (unless report-only)
- calls specialized agent tool wrappers and synthesizes a final response

The implementation uses the wrappers in `agents.tools_wrappers` and the
`QueryClassifier` in `agents.query_classifier`.
"""
from typing import Dict, Any, List
import logging
import time
import json

from .query_classifier import QueryClassifier
from .tools_wrappers import (
    content_retriever_tool,
    content_generator_tool,
    quiz_agent_tool,
    report_agent_tool,
    specialist_agent_tool,
)

log = logging.getLogger(__name__)


ORCHESTRATOR_SYSTEM_PROMPT = """
You are an intelligent orchestrator for a learning platform. Coordinate specialized
agents to provide retrieval, content generation, quizzing, reporting and domain
specialist work. ALWAYS call the retriever first (unless the query is a
performance_report), then call the appropriate downstream agent(s). Synthesize
the results into a coherent final response.

LOGGING POLICY (enforced):
- Every incoming query MUST be logged with timestamp, user_id (if provided), and
  the raw text of the query.
- The query classification decision MUST be logged with the full score vector.
- Every agent invocation MUST be logged with: agent name, input summary (truncated),
  output summary (truncated), duration_ms, and any errors.
- Session loads and saves MUST be logged with session id and sizes.
- The orchestrator MUST emit a final structured log record containing the
  full trace: classification, retrieval output id/summary, each agent output
  and a final synthesized response.

Follow these logging rules strictly and write logs in structured JSON so they
can be consumed by downstream monitoring and audit tools.
"""


class Orchestrator:
    def __init__(self, classifier: QueryClassifier = None):
        self.classifier = classifier or QueryClassifier()

    def _call_retriever(self, query: str, context: str = "") -> str:
        log.debug("Calling retriever for query: %s", query)
        return content_retriever_tool(query=query, context=context)

    def _call_content_generation(self, query: str, retrieved: str) -> str:
        return content_generator_tool(query=query, retrieved_docs=retrieved)

    def _call_quiz(self, query: str, retrieved: str, difficulty: str = "medium") -> str:
        return quiz_agent_tool(query=query, retrieved_docs=retrieved, difficulty=difficulty)

    def _call_report(self, user_id: str, time_period: str = "all") -> str:
        return report_agent_tool(user_id=user_id, time_period=time_period)

    def _call_specialist(self, query: str, retrieved: str) -> str:
        return specialist_agent_tool(query=query, retrieved_docs=retrieved)

    def _synthesize(self, pieces: List[Dict[str, str]]) -> str:
        parts = []
        for p in pieces:
            parts.append(f"[{p['agent'].upper()}]\n{p['output']}\n")
        return "\n---\n".join(parts)

    def process_query(self, query: str, user_id: str = None, context: str = "") -> Dict[str, Any]:
        """Main entry for processing a user query.

        Returns a dict with keys: `query_type`, `scores`, `steps` (list of agent outputs),
        and `final_response`.
        """
        start_ts = int(time.time() * 1000)
        log.info("incoming_query", extra={"extra_json": {"query": query, "user_id": user_id}})

        qtype, scores = self.classifier.classify(query)
        log.info(
            f"classification result - {query} classified as {qtype}",
            extra={"extra_json": {"query": query, "query_type": qtype, "scores": scores}},
        )

        workflow = self.classifier.query_types[qtype]

        steps = []
        retrieved = ""

        # Always call retriever unless workflow is direct/report-only
        if "retriever" in workflow.get("agents", []):
            t0 = time.time()
            retrieved = self._call_retriever(query=query, context=context)
            dur = int((time.time() - t0) * 1000)
            steps.append({"agent": "retriever", "output": retrieved})
            log.info(
                "agent_step",
                extra={
                    "extra_json": {
                        "agent": "retriever",
                        "duration_ms": dur,
                        "output_summary": str(retrieved)[:1000],
                    }
                },
            )

        # Route to agents as per workflow
        for agent_name in workflow.get("agents", []):
            if agent_name == "retriever":
                continue
            t0 = time.time()
            if agent_name == "content_generation":
                out = self._call_content_generation(query=query, retrieved=retrieved)
            elif agent_name == "quiz":
                out = self._call_quiz(query=query, retrieved=retrieved)
            elif agent_name == "report":
                out = self._call_report(user_id=user_id or "unknown")
            elif agent_name == "specialist":
                out = self._call_specialist(query=query, retrieved=retrieved)
            else:
                out = f"[unknown-agent {agent_name}]"
            dur = int((time.time() - t0) * 1000)
            steps.append({"agent": agent_name, "output": out})
            log.info(
                "agent_step",
                extra={
                    "extra_json": {
                        "agent": agent_name,
                        "duration_ms": dur,
                        "output_summary": str(out)[:1000],
                    }
                },
            )

        final_response = self._synthesize(steps)

        # structured orchestrator trace
        trace = {
            "timestamp_ms": start_ts,
            "user_id": user_id,
            "query": query,
            "query_type": qtype,
            "scores": scores,
            "steps": [
                {"agent": s["agent"], "output_summary": str(s["output"])[:1000]} for s in steps
            ],
            "final_response_summary": str(final_response)[:4000],
        }

        log.info("orchestrator_trace", extra={"extra_json": trace})

        return {
            "query": query,
            "query_type": qtype,
            "scores": scores,
            "steps": steps,
            "final_response": final_response,
        }


__all__ = ["Orchestrator", "ORCHESTRATOR_SYSTEM_PROMPT"]
