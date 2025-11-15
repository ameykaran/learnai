# Agents package

This package contains a minimal, modular orchestrator prototype for a
multi-agent learning platform. It is intended as a starting point and uses
safe fallbacks (stubs) if the Strands SDK is not installed.

Files
- `query_classifier.py` – rule-based and LLM-based classifier
- `tools_wrappers.py` – tool-wrapped agent wrappers (use `strands` when available)
- `orchestrator.py` – deterministic orchestrator enforcing workflow rules
- `session_manager.py` – simple filesystem session persistence
- `utils.py` – logging & cache helpers
- `specialist_math_agent.py` – finetuned LiquidAI math model for domain-specific problems
- `system_instruction.txt` – system prompt and logging policy

How to use
1. Install `strands` SDK in your environment (optional). If not installed,
   the package will use stubbed agents that return placeholders.
2. For math problem solving, install `transformers` and `torch`:
   ```bash
   pip install transformers torch
   ```
3. Import `agents.orchestrator.Orchestrator` and call
   `process_query(query, user_id)`.

Example
```python
from agents.orchestrator import Orchestrator
from agents.utils import setup_logging

setup_logging()
orch = Orchestrator()

# Math query will use finetuned LiquidAI model
result = orch.process_query("Solve: integrate x^2", user_id="user_123")
print(result["final_response"])
```

Extending
- Replace `AgentStub` in `tools_wrappers.py` with real `Agent(...)` calls and
  wire your RAG/vector DB/search tools to the retriever wrapper.
- Add more query types and routing rules in `query_classifier.py`.
- Add more specialist agents (e.g., code_specialist, science_specialist) by
  following the pattern in `specialist_math_agent.py`.
