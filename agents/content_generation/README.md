# Content Generation Strands Agent

A Strands AI agent for dynamically generating professional PDF documents and presentation slides from markdown content.

## 🌟 Features

- **PDF Document Generation**: Create professional PDF documents with customizable titles, authors, and dates
- **Presentation Slides**: Generate beautiful 16:9 widescreen slides with gradient backgrounds
- **Markdown Support**: Full markdown syntax support including tables, code blocks, and more
- **AI-Powered**: Uses Strands Agents framework for natural language interaction
- **Multiple Tools**: Three specialized tools for different use cases

## 📦 Installation

### Prerequisites

Install system dependencies for WeasyPrint:

**Ubuntu/Debian:**
```bash
sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**macOS:**
```bash
brew install pango gdk-pixbuf libffi
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Interactive Mode

Run the agent in interactive mode:

```bash
python content_agent.py
```

Example conversation:
```
💬 You: Create a presentation about Python basics with 3 slides
🤔 Agent: [generates slides]

💬 You: Generate a PDF document with title "My Report" and author "John Doe"
🤔 Agent: [generates document]
```

### Programmatic Usage

```python
from content_agent import create_content_agent

# Create the agent
agent = create_content_agent()

# Generate a PDF document
response = agent("Create a PDF document about AI with title 'Introduction to AI'")

# Generate presentation slides
response = agent("Create slides about machine learning. Use this content: ...")

# Convert existing markdown file
response = agent("Convert report.md to a PDF document")
```

## 🛠️ Available Tools

### 1. `generate_pdf_document`

Generate a professional PDF document from markdown content.

**Parameters:**
- `markdown_content` (str): The markdown text to convert
- `output_file` (str): Output PDF file path
- `title` (str, optional): Document title
- `author` (str, optional): Document author
- `date` (str, optional): Document date

**Example:**
```python
response = agent("Generate a PDF with this content: # Hello World\nThis is a test")
```

### 2. `generate_presentation_slides`

Generate presentation slides in 16:9 format.

**Parameters:**
- `markdown_content` (str): Markdown content (use `---` to separate slides)
- `output_file` (str): Output PDF file path

**Example:**
```python
markdown = """
# Introduction
Welcome to the presentation

---

# Main Points
- Point 1
- Point 2
"""
response = agent(f"Create slides with this content: {markdown}")
```

### 3. `convert_markdown_file`

Convert an existing markdown file to PDF or slides.

**Parameters:**
- `input_file` (str): Path to input markdown file
- `output_file` (str): Output PDF file path
- `format_type` (str): Either 'pdf' or 'slides'

**Example:**
```python
response = agent("Convert presentation.md to slides format")
```

## 📝 Markdown Format

### For Documents

Standard markdown with optional YAML front matter:

```markdown
---
title: My Document
author: John Doe
date: 2024-01-01
---

# Introduction

Your content here...

## Section 1

More content...
```

### For Slides

Separate slides using `---` or by starting with `# Heading`:

```markdown
# Title Slide
Welcome!

---

# Second Slide
- Bullet point 1
- Bullet point 2

---

# Third Slide
Content here
```

## 🎨 Styling

### Documents
- Clean, professional styling
- Blue accents (#2563eb)
- Proper spacing and typography
- Tables with alternating row colors
- Syntax-highlighted code blocks

### Slides
- 16:9 widescreen format
- Purple/blue gradient backgrounds
- Large, readable fonts
- Slide numbers
- Math expression support

## 🔧 Configuration

### Model Providers

The agent supports multiple model providers. Configure when creating the agent:

```python
from strands.models import BedrockModel

# Use Amazon Bedrock
agent = create_content_agent(
    model=BedrockModel(model_id='us.anthropic.claude-sonnet-4-20250514-v1:0')
)

# Use OpenAI
from strands.models import OpenAIModel
agent = create_content_agent(
    model=OpenAIModel(model='gpt-4')
)
```

### Custom Instructions

Customize the agent behavior:

```python
agent = create_content_agent(
    instructions="You are a technical writer assistant specialized in creating documentation..."
)
```

## 📊 Examples

### Example 1: Generate Technical Report

```python
agent = create_content_agent()

report = """
# System Architecture

## Overview
Our system consists of three main components...

## Components
1. Frontend
2. Backend
3. Database
"""

response = agent(f"Create a PDF titled 'System Architecture Report' with this content: {report}")
```

### Example 2: Create Training Slides

```python
slides = """
# Welcome
Introduction to Python

---

# Variables
- Python variables are dynamically typed
- No need to declare types

---

# Functions
```python
def greet(name):
    return f"Hello, {name}!"
```
"""

response = agent(f"Generate training slides with this content: {slides}")
```

### Example 3: Convert Existing File

```python
response = agent("Convert my_notes.md to a PDF document at output/notes.pdf")
```

## 📚 API Reference

### `create_content_agent(**kwargs)`

Create a configured Strands agent with content generation tools.

**Parameters:**
- `model`: Model configuration (optional)
- `name`: Agent name (default: "Content Generator")
- `instructions`: Custom system instructions (optional)
- `**kwargs`: Additional Strands Agent parameters

**Returns:**
- Configured `Agent` instance

## 🔗 Resources

- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/docs/)
- [Strands Tools Guide](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/)
- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)

## 📄 License

Same as parent project.

## 🤝 Contributing

Contributions welcome! Feel free to submit issues or pull requests.
