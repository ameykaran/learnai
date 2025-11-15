# Unified Markdown Converter

## Single Tool for PDFs and Slides

The `converter.py` tool handles both PDF documents and presentation slides with simple flags.


### **Basic Commands**
```bash
# Create PDF document
python3 converter.py input.md output.pdf --pdf

# Create presentation slides
python3 converter.py input.md output.pdf --slides
```

## Features

- **PDF Documents**: Professional styling, tables, code blocks
- **Presentation Slides**: Widescreen format, no formatting issues
- **Single Tool**: One command with --pdf or --slides flag
- **Agent Ready**: Simple interface for AI integration

## potential agent integration

```python
import subprocess

def convert_markdown(input_file, output_file, format_type):
    """Agent function to convert markdown."""
    cmd = ["python3", "converter.py", input_file, output_file, f"--{format_type}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

# Usage
convert_markdown("report.md", "report.pdf", "pdf")
convert_markdown("presentation.md", "slides.pdf", "slides")
```

