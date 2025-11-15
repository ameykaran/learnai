#!/usr/bin/env python3
"""
Content Generation Agent using Strands Framework
Provides tools for generating PDF documents and presentation slides from markdown content.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from strands import Agent, tool
from strands.models import BedrockModel
import os
import markdown
import weasyprint
import yaml
from jinja2 import Template
import logging

# Set up logger
logger = logging.getLogger(__name__)



class ContentGenerator:
    """Handles the actual PDF and slide generation logic."""

    def __init__(self):
        self.setup_themes()

    def setup_themes(self):
        """Setup CSS themes for documents and slides."""
        self.document_css = """
body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    max-width: 800px; margin: 0 auto; padding: 2rem;
    line-height: 1.6; color: #333; font-size: 16px;
}

h1 {
    color: #2563eb; border-bottom: 3px solid #2563eb;
    padding-bottom: 0.5rem; margin-bottom: 2rem;
    font-size: 2.5rem; font-weight: 700;
}

h2 {
    color: #2563eb; border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.25rem; font-size: 2rem;
}

h3 { color: #64748b; font-size: 1.5rem; }

code {
    background: #f8fafc; padding: 0.125rem 0.25rem;
    border-radius: 0.25rem; font-family: Monaco, monospace;
    border: 1px solid #e2e8f0;
}

pre {
    background: #f8fafc; padding: 1rem; border-radius: 0.5rem;
    overflow-x: auto; border: 1px solid #e2e8f0;
}

blockquote {
    border-left: 4px solid #06b6d4; padding-left: 1rem;
    margin: 1.5rem 0; font-style: italic; color: #64748b;
    background: #f0f9ff; padding: 1rem;
}

table {
    width: 100%; border-collapse: collapse; margin: 1.5rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

th, td { border: 1px solid #e2e8f0; padding: 0.75rem; text-align: left; }
th { background: #2563eb; color: white; font-weight: 600; }
tr:nth-child(even) { background: #f8fafc; }

.document-footer {
    text-align: center; margin-top: 3rem; padding-top: 2rem;
    border-top: 1px solid #e2e8f0; color: #64748b; font-size: 0.875rem;
}
"""

        self.slides_css = """
@page { size: 16in 9in; margin: 0; }

body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 0; }

.slide {
    height: 9in; width: 16in; padding: 2.5rem 3rem;
    display: flex; flex-direction: column; justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; page-break-after: always; position: relative;
    box-sizing: border-box; overflow: hidden;
}

.slide:first-child {
    background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
    text-align: center;
}

.slide h1 {
    font-size: 3.5rem; font-weight: 700; margin-bottom: 2rem;
    color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.slide h2 {
    font-size: 2.5rem; font-weight: 600; margin-bottom: 1.5rem; color: #f8fafc;
}

.slide h3 {
    font-size: 2rem; font-weight: 500; margin-bottom: 1rem; color: #e2e8f0;
}

.slide p { font-size: 1.5rem; line-height: 1.6; margin: 1rem 0; }

.slide ul, .slide ol {
    font-size: 1.4rem; line-height: 1.8; margin: 1rem 0; padding-left: 2rem;
}

.slide li { margin: 0.8rem 0; }

.slide table {
    background: white; color: #333; border-radius: 0.5rem;
    overflow: hidden; margin: 2rem 0; width: 100%; font-size: 1.2rem;
}

.slide th {
    background: #1e40af; color: white; padding: 1rem; font-weight: 600;
}

.slide td { padding: 1rem; border-bottom: 1px solid #e5e5e5; }

.slide code {
    background: rgba(255,255,255,0.2); color: #fbbf24;
    padding: 0.25rem 0.5rem; border-radius: 0.25rem;
    font-family: Monaco, monospace; font-size: 1.2rem;
}

.slide pre {
    background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 0.5rem;
    overflow-x: auto; margin: 1.5rem 0;
}

.slide pre code { background: none; color: #e5e5e5; padding: 0; }

.slide blockquote {
    background: rgba(255,255,255,0.1); border-left: 4px solid #fbbf24;
    padding: 1rem 2rem; margin: 2rem 0; font-style: italic; border-radius: 0.25rem;
}

.slide-number {
    position: absolute; bottom: 1rem; right: 2rem; font-size: 0.9rem; opacity: 0.8;
    background: rgba(0,0,0,0.3); padding: 0.3rem 0.6rem; border-radius: 0.3rem;
}

.math {
    font-size: 1.3rem; color: #fbbf24; background: rgba(0,0,0,0.2);
    padding: 0.5rem; border-radius: 0.25rem; display: inline-block;
}
"""

    def create_document(self, markdown_content: str, title: str = "Document", 
                       author: str = "", date: str = "") -> str:
        """Create PDF document from markdown content."""
        # Parse front matter if present
        content, metadata = self._parse_front_matter(markdown_content)
        
        # Override metadata with provided parameters
        if title:
            metadata['title'] = title
        if author:
            metadata['author'] = author
        if date:
            metadata['date'] = date

        # Convert markdown to HTML
        md = markdown.Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc'
        ])

        html_content = md.convert(content)

        # Create complete HTML document
        template = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>{{ css }}</style>
</head>
<body>
    <div class="document">
        {% if title and title != 'Document' %}
        <h1 class="document-title">{{ title }}</h1>
        {% endif %}
        {% if author %}
        <p class="document-author"><strong>Author:</strong> {{ author }}</p>
        {% endif %}
        {% if date %}
        <p class="document-date"><strong>Date:</strong> {{ date }}</p>
        {% endif %}

        <div class="document-content">
            {{ content | safe }}
        </div>

        <div class="document-footer">
            <p>Generated on {{ timestamp }}</p>
        </div>
    </div>
</body>
</html>
        """)

        html_doc = template.render(
            title=metadata.get('title', 'Document'),
            author=metadata.get('author', ''),
            date=metadata.get('date', ''),
            content=html_content,
            css=self.document_css,
            timestamp=self._get_timestamp()
        )

        # Convert to PDF
        return self._html_to_pdf(html_doc)

    def create_slides(self, markdown_content: str) -> str:
        """Create presentation slides from markdown content."""
        # Remove YAML front matter if present
        content = markdown_content
        if content.startswith('---'):
            try:
                end_idx = content.index('---', 3)
                content = content[end_idx + 3:].strip()
            except ValueError:
                pass

        # Split into slides
        slides = self._split_into_slides(content)

        # Generate slide HTML
        html_content = self._generate_slide_html(slides)

        # Convert to PDF
        return self._html_to_pdf(html_content)

    def _split_into_slides(self, content):
        """Split content into slides."""
        slides = []
        current_slide = []

        for line in content.split('\n'):
            if line.strip() == '---':
                if current_slide:
                    slides.append('\n'.join(current_slide))
                    current_slide = []
            elif line.startswith('# ') and current_slide:
                if current_slide:
                    slides.append('\n'.join(current_slide))
                    current_slide = []
                current_slide.append(line)
            else:
                current_slide.append(line)

        if current_slide:
            slides.append('\n'.join(current_slide))

        return slides if slides else [content]

    def _generate_slide_html(self, slides):
        """Generate HTML for slides."""
        html_slides = []
        md = markdown.Markdown(extensions=['tables', 'fenced_code'])

        for i, slide_content in enumerate(slides):
            slide_html = md.convert(slide_content.strip())

            # Handle math expressions
            slide_html = slide_html.replace('\\[', '<div class="math">').replace('\\]', '</div>')
            slide_html = slide_html.replace('\\(', '<span class="math">').replace('\\)', '</span>')

            slide_div = f'''
<div class="slide">
    {slide_html}
    <div class="slide-number">{i + 1} / {len(slides)}</div>
</div>
'''
            html_slides.append(slide_div)

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Presentation Slides</title>
    <style>{self.slides_css}</style>
</head>
<body>
{''.join(html_slides)}
</body>
</html>"""

    def _parse_front_matter(self, content):
        """Parse YAML front matter."""
        metadata = {}
        if content.startswith('---'):
            try:
                end_idx = content.index('---', 3)
                front_matter = content[3:end_idx].strip()
                metadata = yaml.safe_load(front_matter) or {}
                content = content[end_idx + 3:].strip()
            except (ValueError, yaml.YAMLError):
                pass
        return content, metadata

    def _html_to_pdf(self, html_content):
        """Convert HTML to PDF using WeasyPrint and return base64."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_html_path = f.name

        try:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as pdf_file:
                temp_pdf_path = pdf_file.name
            
            document = weasyprint.HTML(filename=temp_html_path)
            document.write_pdf(temp_pdf_path)
            
            # Read PDF and return base64
            with open(temp_pdf_path, 'rb') as f:
                import base64
                pdf_data = base64.b64encode(f.read()).decode('utf-8')
            
            return pdf_data
        finally:
            os.unlink(temp_html_path)
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)

    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Initialize generator
generator = ContentGenerator()


# Define Strands Agent Tools
@tool
def generate_pdf_document(markdown_content: str, output_file: str, 
                         title: str = "Document", 
                         author: str = "", 
                         date: str = "") -> str:
    """Generate a professional PDF document from markdown content.
    
    Args:
        markdown_content: The markdown text to convert to PDF
        output_file: Path where the PDF file should be saved
        title: Document title (optional)
        author: Document author (optional)
        date: Document date (optional)
    """
    try:
        # Generate PDF
        pdf_base64 = generator.create_document(markdown_content, title, author, date)
        
        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        import base64
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(pdf_base64))
        
        return f"✅ Successfully generated PDF document at: {output_path.absolute()}\n" \
               f"Title: {title}\n" \
               f"Size: {output_path.stat().st_size / 1024:.2f} KB"
    
    except Exception as e:
        return f"❌ Error generating PDF document: {str(e)}"


@tool
def generate_presentation_slides(markdown_content: str, output_file: str) -> str:
    """Generate presentation slides (16:9 widescreen PDF) from markdown content.
    
    Use '---' or '# Heading' to separate slides. The markdown will be converted
    to beautiful presentation slides with gradient backgrounds.
    
    Args:
        markdown_content: The markdown text to convert to slides (use --- to separate slides)
        output_file: Path where the PDF slides should be saved
    """
    try:
        # Generate slides
        pdf_base64 = generator.create_slides(markdown_content)
        
        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        import base64
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(pdf_base64))
        
        # Count slides
        slide_count = markdown_content.count('---') + markdown_content.count('# ')
        
        return f"✅ Successfully generated presentation slides at: {output_path.absolute()}\n" \
               f"Approximate slides: {slide_count}\n" \
               f"Size: {output_path.stat().st_size / 1024:.2f} KB"
    
    except Exception as e:
        return f"❌ Error generating slides: {str(e)}"


@tool
def convert_markdown_file(input_file: str, output_file: str, format_type: str) -> str:
    """Convert a markdown file to PDF document or presentation slides.
    
    Args:
        input_file: Path to the input markdown file
        output_file: Path where the output PDF should be saved
        format_type: Either 'pdf' for document or 'slides' for presentation
    """
    try:
        input_path = Path(input_file)
        
        if not input_path.exists():
            return f"❌ Error: Input file not found: {input_file}"
        
        # Read markdown content
        markdown_content = input_path.read_text(encoding='utf-8')
        
        # Convert based on format type
        if format_type.lower() == 'slides':
            return generate_presentation_slides(markdown_content, output_file)
        else:
            # Parse front matter for metadata
            metadata = {}
            if markdown_content.startswith('---'):
                try:
                    end_idx = markdown_content.index('---', 3)
                    front_matter = markdown_content[3:end_idx].strip()
                    metadata = yaml.safe_load(front_matter) or {}
                except:
                    pass
            
            return generate_pdf_document(
                markdown_content, 
                output_file,
                title=metadata.get('title', 'Document'),
                author=metadata.get('author', ''),
                date=metadata.get('date', '')
            )
    
    except Exception as e:
        return f"❌ Error converting file: {str(e)}"


def create_content_agent(**kwargs):
    """Create a Strands agent with content generation tools.
    
    Args:
        model_provider: Optional model provider configuration
        **kwargs: Additional agent configuration options
    
    Returns:
        Configured Strands Agent
    """
    agent_config = {
        'name': 'Content Generator',
        'description': 'An AI agent that generates professional PDF documents and presentation slides from markdown content.',
        'tools': [generate_pdf_document, generate_presentation_slides, convert_markdown_file],
        'system_prompt': """You are a content generation assistant that helps users create professional 
PDF documents and presentation slides from markdown content.

You have three main capabilities:
1. Generate PDF documents with proper formatting, titles, authors, and dates
2. Create presentation slides in 16:9 widescreen format with beautiful gradients
3. Convert existing markdown files to either format

When users ask for documents, use generate_pdf_document(). 
When users ask for slides or presentations, use generate_presentation_slides().
For file conversions, use convert_markdown_file().

Always ask for clarification if the output format is unclear."""
    }
    
    # Merge with any additional config
    agent_config.update(kwargs)

    # Create a configured Bedrock model
    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        streaming=False,
    )

    try:
        agent = Agent(model=model, **agent_config)
        logger.info("✅ Agent created successfully with 5 tools")
    except Exception as e:
        logger.error(f"❌ Failed to create Agent/BedrockModel: {e}")
        raise
    return agent

def main():
    """Interactive CLI for the content generation agent."""
    print("🤖 Content Generation Agent")
    print("=" * 50)
    print("I can help you generate PDF documents and presentation slides!")
    print("Type 'quit' or 'exit' to stop.\n")
    
    try:
        agent = create_content_agent()
        
        while True:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Run agent
            print("\n🤔 Agent:", end=" ")
            response = agent(user_input)
            print(response)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
