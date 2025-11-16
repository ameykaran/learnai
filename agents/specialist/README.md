# Specialist Math Agent

A Strands-based agent for advanced mathematical problem solving using the LiquidAI LFM2-350M-Math finetuned model.

## Overview

The Specialist Math Agent is designed to solve complex mathematical problems with step-by-step explanations. It uses a specialized language model finetuned on mathematical reasoning tasks and can leverage context from the RAG system for improved accuracy.

## Features

- **Advanced Problem Solving**: Handles algebra, calculus, probability, geometry, and more
- **Step-by-Step Explanations**: Provides detailed working and reasoning
- **Context Integration**: Uses examples and theory from the knowledge base
- **Solution Verification**: Can verify and critique proposed solutions
- **Educational Focus**: Explains concepts, not just answers

## Architecture

```
agents/specialist/
├── __init__.py          # Package initialization
├── agent.py            # Main SpecialistMathAgent class
├── config.py           # Configuration and constants
├── prompts.py          # System prompts and templates
└── tools.py            # Strands tools for problem solving
```

## Usage

### Basic Usage

```python
from agents.specialist import SpecialistMathAgent

# Create the agent
agent = SpecialistMathAgent()

# Solve a problem
response = agent("Find the derivative of f(x) = x^3 + 2x^2 - 5x + 3")
print(response)
```

### With Context from RAG

```python
from agents.specialist import SpecialistMathAgent
from agents.retrieval import RAGChatAgent

# Initialize agents
rag_agent = RAGChatAgent()
specialist = SpecialistMathAgent()

# Get context from RAG
context = rag_agent.search_knowledge_base(
    query="conditional probability",
    chunk_type="example",
    k=2
)

# Solve with context
problem = "Calculate P(A|B) given P(A)=0.3, P(B)=0.4, P(A∩B)=0.12"
response = specialist(problem, context=context)
print(response)
```

### Using Individual Tools

The agent provides two main tools:

#### 1. solve_math_problem

```python
from agents.specialist.tools import solve_math_problem

# Simple problem
result = solve_math_problem("Solve for x: 2x + 5 = 13")

# With context
result = solve_math_problem(
    problem="Integrate ∫(x^2 + 3x) dx",
    context="Remember: ∫x^n dx = x^(n+1)/(n+1) + C"
)
```

#### 2. verify_solution

```python
from agents.specialist.tools import verify_solution

result = verify_solution(
    problem="Solve: 3x - 7 = 14",
    solution="3x = 21, therefore x = 7"
)
```

## Capabilities

The agent excels at:

### Algebra
- Solving equations and inequalities
- Factoring polynomials
- Systems of equations
- Algebraic manipulation

### Calculus
- Derivatives (power rule, chain rule, product rule)
- Integrals (indefinite and definite)
- Limits and continuity
- Series and sequences

### Probability & Statistics
- Probability calculations
- Conditional probability
- Expected value and variance
- Distributions (normal, binomial, etc.)

### Geometry & Trigonometry
- Geometric proofs
- Coordinate geometry
- Trigonometric identities
- Angle and distance calculations

### Word Problems
- Setting up equations from word problems
- Mathematical modeling
- Multi-step reasoning

## Configuration

Adjust model behavior in `config.py`:

```python
# Model settings
MODEL_ID = "LiquidAI/LFM2-350M-Math"
MODEL_TEMPERATURE = 0.6        # Lower = more focused, Higher = more creative
MODEL_TOP_P = 0.95            # Nucleus sampling parameter
MODEL_MAX_NEW_TOKENS = 1024   # Maximum response length

# Agent settings
AGENT_NAME = "specialist_math_agent"
```

## Integration with Orchestrator

The specialist agent is designed to work with the orchestrator system:

```python
from agents.orchestrator import WorkflowOrchestrator

# The orchestrator will automatically route to specialist for:
# - "domain_query" type questions
# - Mathematical problem-solving requests
# - Questions requiring step-by-step calculations

orchestrator = WorkflowOrchestrator()
response = orchestrator("Solve the quadratic equation: x^2 - 5x + 6 = 0")
```

The orchestrator classifies queries and routes them appropriately:
- **"teach me probability"** → retrieval + content_generation
- **"solve this equation"** → retrieval + specialist
- **"quiz me on calculus"** → retrieval + quiz

## Performance Optimization

### Model Loading

The model is lazy-loaded on first use and cached for subsequent calls:
- First call: ~10-30 seconds (model download + loading)
- Subsequent calls: <1 second (cached)

### Memory Usage

- Model size: ~1.4GB on disk
- GPU memory: ~2-3GB during inference
- CPU RAM: ~4-6GB if running on CPU

### Inference Speed

- GPU (CUDA): 1-3 seconds per problem
- CPU: 5-15 seconds per problem

## Examples

### Example 1: Algebraic Equation

```python
agent = SpecialistMathAgent()
response = agent("""
Solve the system of equations:
2x + 3y = 12
x - y = 1
""")
```

### Example 2: Calculus with Context

```python
context = """
Chain Rule: If y = f(g(x)), then dy/dx = f'(g(x)) · g'(x)
Example: d/dx[sin(x²)] = cos(x²) · 2x
"""

response = agent(
    "Find the derivative of h(x) = sin(3x² + 1)",
    context=context
)
```

### Example 3: Probability

```python
response = agent("""
A fair die is rolled twice. What is the probability that:
a) Both rolls show even numbers?
b) The sum of the rolls is 7?
c) The second roll is greater than the first?
""")
```

## Limitations

- **Mathematical Notation**: Works best with clear text notation (use ^ for exponents, not superscripts)
- **Diagram Generation**: Cannot create visual diagrams or plots
- **Symbolic Computation**: May struggle with very complex symbolic manipulations
- **Proof Complexity**: Better at computational problems than abstract proofs
- **Context Length**: Limited to ~1024 tokens per response

## Future Enhancements

- [ ] Integration with symbolic math libraries (SymPy)
- [ ] Support for diagram/graph generation
- [ ] LaTeX output formatting
- [ ] Difficulty level adaptation
- [ ] Multi-step problem decomposition
- [ ] Interactive problem-solving mode

## Contributing

When extending the specialist agent:

1. Add new tools in `tools.py` using the `@tool` decorator
2. Update `SYSTEM_PROMPT` in `config.py` for new capabilities
3. Test with diverse mathematical problems
4. Document tool usage and examples

## References

- **Model**: [LiquidAI/LFM2-350M-Math](https://huggingface.co/LiquidAI/LFM2-350M-Math)
- **Framework**: [Strands](https://strandsagents.com/)
- **Transformers**: [HuggingFace Transformers](https://huggingface.co/docs/transformers/)

## License

This agent implementation follows the same license as the parent project.

---

**Need Help?** Check the examples in `run_specialist_agent.py` or see the main project documentation.
