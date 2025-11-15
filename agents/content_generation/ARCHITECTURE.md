# System Architecture

## Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Content Generation Agent                  │
│                     (Strands Framework)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PDF Tool    │    │  Slides Tool │    │ Convert Tool │
│              │    │              │    │              │
│ @tool        │    │ @tool        │    │ @tool        │
│ decorator    │    │ decorator    │    │ decorator    │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ ContentGenerator │
                    │                  │
                    │ • setup_themes() │
                    │ • create_doc()   │
                    │ • create_slides()│
                    └──────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌───────────┐  ┌──────────┐  ┌──────────┐
        │ Markdown  │  │ Jinja2   │  │WeasyPrint│
        │ Parser    │  │Templates │  │  PDF     │
        └───────────┘  └──────────┘  └──────────┘
```

## Data Flow

### PDF Document Generation

```
User Request
    │
    ▼
"Create a PDF about AI"
    │
    ▼
Strands Agent
    │
    ▼
generate_pdf_document(
  markdown_content="...",
  output_file="ai_report.pdf",
  title="AI Report"
)
    │
    ▼
ContentGenerator.create_document()
    │
    ├─► Parse YAML front matter
    ├─► Convert Markdown → HTML
    ├─► Apply CSS styling
    ├─► Render with Jinja2
    └─► WeasyPrint → PDF
         │
         ▼
    ai_report.pdf
         │
         ▼
    Success Message ✅
```

### Presentation Slides Generation

```
User Request
    │
    ▼
"Generate slides about Python"
    │
    ▼
Strands Agent
    │
    ▼
generate_presentation_slides(
  markdown_content="...",
  output_file="python_slides.pdf"
)
    │
    ▼
ContentGenerator.create_slides()
    │
    ├─► Split content by "---"
    ├─► Process each slide
    ├─► Convert Markdown → HTML
    ├─► Apply gradient CSS
    ├─► Add slide numbers
    └─► WeasyPrint → PDF
         │
         ▼
    python_slides.pdf
         │
         ▼
    Success Message ✅
```

## Usage Patterns

### Pattern 1: Direct Tool Usage

```python
from content_agent import generate_pdf_document

# Direct function call (no agent)
result = generate_pdf_document(
    markdown_content="# Hello",
    output_file="hello.pdf"
)

# No LLM needed ✅
# Fast execution ✅
# Programmatic control ✅
```

### Pattern 2: AI Agent Interface

```python
from content_agent import create_content_agent

agent = create_content_agent()

# Natural language
response = agent("Create a PDF about cats")

# LLM interprets request ✅
# Flexible input ✅
# Conversational ✅
```

### Pattern 3: Multi-Agent System

```python
from strands import Agent
from content_agent import generate_pdf_document

research_agent = Agent(
    name="Researcher",
    instructions="Research topics..."
)

report_agent = Agent(
    name="Reporter", 
    tools=[generate_pdf_document],
    instructions="Create reports..."
)

# Research → Generate Report
research = research_agent("Research AI trends")
report_agent(f"Create report about: {research}")
```

## Tool Specifications

### Tool 1: generate_pdf_document

```
Input Schema:
{
  "markdown_content": string (required),
  "output_file": string (required),
  "title": string (optional, default="Document"),
  "author": string (optional, default=""),
  "date": string (optional, default="")
}

Output:
{
  "status": "success" | "error",
  "content": [{"text": "✅ Success message..."}]
}
```

### Tool 2: generate_presentation_slides

```
Input Schema:
{
  "markdown_content": string (required),
  "output_file": string (required)
}

Output:
{
  "status": "success" | "error",
  "content": [{"text": "✅ Success message..."}]
}
```

### Tool 3: convert_markdown_file

```
Input Schema:
{
  "input_file": string (required),
  "output_file": string (required),
  "format_type": string (required, "pdf" | "slides")
}

Output:
{
  "status": "success" | "error",
  "content": [{"text": "✅ Success message..."}]
}
```

## File Structure

```
tools/ContentGeneration/
│
├── content_agent.py          # Main agent (580 lines)
│   ├── ContentGenerator      # Generation logic
│   ├── @tool functions        # Strands tools
│   ├── create_content_agent() # Agent factory
│   └── main()                 # Interactive CLI
│
├── converter.py               # Old CLI tool (382 lines)
│
├── requirements.txt           # Dependencies
│
├── README.md                  # Full documentation
├── QUICKSTART.md             # Quick start guide
├── IMPLEMENTATION.md         # This summary
├── ARCHITECTURE.md           # This file
├── CONVERTER_USAGE.md        # Comparison guide
│
├── examples.py               # Usage examples
└── test_setup.py             # Setup verification

Output/
├── *.pdf                     # Generated PDFs
└── *.md                      # Sample markdown
```

## Technology Stack

```
┌─────────────────────────────────┐
│     Strands Agents Framework    │  ← AI orchestration
└─────────────────────────────────┘
              │
┌─────────────┴─────────────┐
│                           │
▼                           ▼
┌──────────────┐    ┌──────────────┐
│ LLM Provider │    │  Tool Layer  │
│              │    │              │
│ • Bedrock    │    │ • Python     │
│ • OpenAI     │    │ • @tool      │
│ • Anthropic  │    │ • Type hints │
└──────────────┘    └──────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌──────────────┐                    ┌──────────────┐
│  Processing  │                    │   Rendering  │
│              │                    │              │
│ • Markdown   │                    │ • Jinja2     │
│ • YAML       │                    │ • WeasyPrint │
│ • Python     │                    │ • CSS        │
└──────────────┘                    └──────────────┘
```

## Performance Characteristics

### PDF Document Generation
- **Speed**: ~1-2 seconds for typical document
- **Memory**: ~50-100 MB
- **Output Size**: Varies (typically 100-500 KB)

### Presentation Slides
- **Speed**: ~2-3 seconds for 5-10 slides
- **Memory**: ~100-200 MB
- **Output Size**: Larger than docs (graphics)

### Agent Response
- **Speed**: Depends on LLM provider
- **Latency**: +0.5-3 seconds for LLM call
- **Memory**: +100-200 MB for agent

## Error Handling

```python
Try:
    Generate content
    ↓
    Success ✅
    ↓
    Return success message
    
Except Exception:
    ↓
    Catch error ❌
    ↓
    Return error message
    ↓
    User gets feedback
```

## Monitoring & Observability

Strands provides built-in:
- **Tracing**: Track agent execution
- **Logging**: Detailed logs
- **Metrics**: Performance data
- **Events**: Tool invocations

```python
from strands.telemetry import enable_tracing

enable_tracing()
agent = create_content_agent()
# All calls are traced automatically
```

## Security Considerations

1. **Input Validation**: Markdown content sanitized
2. **File Paths**: Output paths validated
3. **Resource Limits**: Memory/time limits
4. **Credentials**: Model provider keys secured
5. **Sandboxing**: Tools run in controlled environment

## Summary

A well-architected Strands agent that:
- ✅ Follows Strands best practices
- ✅ Provides multiple usage patterns
- ✅ Has clear separation of concerns
- ✅ Includes comprehensive tooling
- ✅ Ready for production use
- ✅ Easy to extend and maintain
