# Specialist Math Agent - Quick Start Guide

Get started with the Specialist Math Agent in 5 minutes!

## Prerequisites

```bash
# Install required packages
pip install strands transformers torch
```

## Basic Usage

### 1. Import and Initialize

```python
from agents.specialist import get_specialist_agent

# Get the agent (downloads model on first use)
agent = get_specialist_agent()
```

### 2. Solve a Problem

```python
# Simple algebra
response = agent("Solve for x: 2x + 5 = 13")
print(response)
```

### 3. With Context

```python
# Provide helpful context
context = "Remember: P(A|B) = P(A∩B) / P(B)"
problem = "Calculate P(A|B) if P(A∩B) = 0.12 and P(B) = 0.4"

response = agent(problem, context=context)
print(response)
```

## Run Examples

```bash
# Run all examples
python run_specialist_agent.py

# Interactive mode
python run_specialist_agent.py --interactive

# Run tests
python test_specialist_agent.py
```

## Common Use Cases

### Algebra

```python
agent("Solve the system: 2x + 3y = 12, x - y = 1")
```

### Calculus

```python
agent("Find the derivative of f(x) = sin(x^2)")
```

### Probability

```python
agent("A coin is flipped 3 times. What's the probability of getting exactly 2 heads?")
```

### Word Problems

```python
agent("A train travels 60 miles at 40 mph, then 80 miles at 50 mph. What's the average speed?")
```

## Integration with RAG

```python
from agents.retrieval import RAGChatAgent
from agents.specialist import get_specialist_agent

# Get context from knowledge base
rag = RAGChatAgent()
context = rag.search_knowledge_base(
    "conditional probability",
    chunk_type="example",
    k=2
)

# Solve with context
specialist = get_specialist_agent()
response = specialist(
    "Explain how to use Bayes theorem",
    context=context
)
```

## Using Individual Tools

```python
from agents.specialist.tools import solve_math_problem, verify_solution

# Solve a problem
solution = solve_math_problem("Integrate: ∫(x^2 + 3x) dx")

# Verify a solution
verification = verify_solution(
    problem="Solve: 3x + 7 = 22",
    solution="3x = 15, so x = 5"
)
```

## Tips

1. **Be Specific**: State clearly what you want (solve, find, calculate, prove)
2. **Use Plain Text**: Use `^` for exponents (x^2), `/` for fractions (1/2)
3. **Provide Context**: Give relevant formulas or examples when available
4. **Break Down**: For complex problems, break into steps
5. **Check Units**: Specify units in word problems

## Troubleshooting

### Model Not Loading
```bash
# Check internet connection (needed for first download)
# Check disk space (~1.4GB needed)
# Try manual download:
huggingface-cli download LiquidAI/LFM2-350M-Math
```

### Out of Memory
```python
# Use smaller max_tokens
from agents.specialist.tools import solve_math_problem

solve_math_problem("your problem", max_tokens=512)
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade transformers torch strands
```

## Next Steps

- Read the full [README](README.md) for detailed documentation
- Check [examples](run_specialist_agent.py) for more use cases
- See [orchestrator integration](../orchestrator/README.md) for workflow routing
- Explore [RAG integration](../retrieval/README.md) for context-aware solving

## Getting Help

1. Check the logs (set `logging.basicConfig(level=logging.DEBUG)`)
2. Run tests: `python test_specialist_agent.py`
3. Try interactive mode: `python run_specialist_agent.py --interactive`
4. Review the [full documentation](README.md)

---

**Ready to solve some math? Let's go! 🚀**
