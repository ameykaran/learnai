"""Small runner to exercise the DeterministicOrchestrator."""
from agents.orchestrator import Orchestrator
from agents.utils import setup_logging


def main():
    # enable structured logging to logs/agents.jsonl
    setup_logging()
    orch = Orchestrator()

    test_queries = [
        # "Explain how neural networks work",
        # "Create a quiz on Python loops",
        # "Show my progress this month",
        "Solve this calculus problem: integrate x^2",
        # "Generate a lesson plan on databases",
    ]

    for q in test_queries:
        print("\n" + "=" * 60)
        print("Query:", q)
        out = orch.process_query(q, user_id="user_123")
        print(f"Classified as: {out['query_type']}")
        print("Final Response:\n", out["final_response"])


if __name__ == "__main__":
    main()
