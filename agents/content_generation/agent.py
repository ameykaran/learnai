#!/usr/bin/env python3
"""
Content Generation Agent using Strands Framework
Provides tools for generating PDF documents and presentation slides from markdown content.
Now supports LaTeX math using KaTeX (no Chromium required).
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from strands import Agent, tool
from strands.models import BedrockModel
import os
import re
import markdown
import weasyprint
import yaml
from jinja2 import Template
import logging

import shutil
import subprocess
import tempfile

from prompts import AGENT_INSTRUCTIONS

logger = logging.getLogger(__name__)

# -------------------------
#   NODE/KATEX BACKEND
# -------------------------

def check_node_and_katex():
    node_path = shutil.which("node")
    if not node_path:
        return False, "Node.js not found on PATH."

    cmd = [
        "node", "-e",
        "try{require('katex'); console.log('__OK__');}catch(e){process.exit(2)}"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if "__OK__" in proc.stdout:
        return True, "Node+KaTeX OK"
    return False, "KaTeX not available to Node (`npm install katex`)."

NODE_RENDERER_JS = r"""
const fs = require('fs');
const katex = require('katex');
const input = fs.readFileSync(0, 'utf8');
const mode = process.argv[2] === 'display';
try {
  const out = katex.renderToString(input, { displayMode: mode, throwOnError: false });
  process.stdout.write(out);
} catch (err) {
  process.stdout.write(JSON.stringify({error: String(err)}));
  process.exit(1);
}
"""

def render_with_node_katex(latex: str, display: bool, renderer_path: Path):
    mode = "display" if display else "inline"
    proc = subprocess.run(
        ["node", str(renderer_path), mode],
        input=latex, text=True,
        capture_output=True, timeout=10
    )
    if proc.returncode == 0:
        return True, proc.stdout
    return False, proc.stdout or proc.stderr


def convert_math(text: str) -> str:
    # 1) Convert $...$ and $$...$$ → brackets
    ESC = "__ESC_DOLLAR__"
    text = text.replace(r"\$", ESC)

    text = re.sub(r"\$\$(.+?)\$\$", lambda m: f"\\[{m.group(1)}\\]", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\$)\$(.+?)(?<!\$)\$(?!\$)",
                  lambda m: f"\\({m.group(1)}\\)", text, flags=re.DOTALL)

    text = text.replace(ESC, r"\$")

    # 2) Create Node renderer
    tmp_dir = Path.cwd() / "_katex_node"
    tmp_dir.mkdir(exist_ok=True)
    renderer = tmp_dir / "katex_renderer.js"
    renderer.write_text(NODE_RENDERER_JS)

    # 3) Replace display math \[...\]
    def repl_display(m):
        latex = m.group(1)
        ok, out = render_with_node_katex(latex, True, renderer)
        if not ok:
            return f"<pre>KaTeX error: {out}</pre>"
        return f'<div class="katex-display">{out}</div>'

    text = re.sub(r"\\\[(.+?)\\\]", repl_display, text, flags=re.DOTALL)

    # 4) Replace inline math \(...\)
    def repl_inline(m):
        latex = m.group(1)
        ok, out = render_with_node_katex(latex, False, renderer)
        if not ok:
            return f"<code>KaTeX error: {out}</code>"
        return out

    text = re.sub(r"\\\((.+?)\\\)", repl_inline, text, flags=re.DOTALL)

    return text

# -------------------------------
#     MAIN CONTENT GENERATOR
# -------------------------------

class ContentGenerator:
    """Handles PDF document and slide generation."""

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

    # -----------------------
    #   PDF DOCUMENT CREATOR
    # -----------------------
    def create_document(self, markdown_content: str, title: str = "Document",
                        author: str = "LearnAI", date: str = "") -> str:

        content, metadata = self._parse_front_matter(markdown_content)

        metadata['title'] = title or metadata.get('title', 'Document')
        metadata['author'] = author or metadata.get('author', '')
        metadata['date'] = date or metadata.get('date', '')

        md = markdown.Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc',
        ])
    
        html_content = md.convert(content)
        html_content = convert_math(html_content)

        template = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css">
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
            title=metadata.get('title'),
            author=metadata.get('author'),
            date=metadata.get('date'),
            content=html_content,
            css=self.document_css,
            timestamp=self._get_timestamp()
        )

        return self._html_to_pdf(html_doc)

    # ------------------------
    #   SLIDE PDF GENERATOR
    # ------------------------
    def create_slides(self, markdown_content: str) -> str:
        content = markdown_content
        if content.startswith('---'):
            try:
                end_idx = content.index('---', 3)
                content = content[end_idx + 3:].strip()
            except ValueError:
                pass

        slides = self._split_into_slides(content)
        html_content = self._generate_slide_html(slides)
        return self._html_to_pdf(html_content)

    def _split_into_slides(self, content):
        slides = []
        current = []

        for line in content.split('\n'):
            if line.strip() == '---':
                if current:
                    slides.append('\n'.join(current))
                    current = []
            elif line.startswith('# ') and current:
                slides.append('\n'.join(current))
                current = [line]
            else:
                current.append(line)

        if current:
            slides.append('\n'.join(current))

        return slides or [content]

    def _generate_slide_html(self, slides):
        html_slides = []
        md = markdown.Markdown(extensions=['tables', 'fenced_code'])

        for i, slide_md in enumerate(slides):
            slide_html = md.convert(slide_md.strip())
            slide_html = convert_math(slide_html)

            slide_div = f"""
<div class="slide">
    {slide_html}
    <div class="slide-number">{i + 1} / {len(slides)}</div>
</div>
"""
            html_slides.append(slide_div)

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Presentation Slides</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css">
    <style>{self.slides_css}</style>
</head>
<body>
{''.join(html_slides)}
</body>
</html>"""


    # ------------------------
    #  Front Matter + Utils
    # ------------------------
    def _parse_front_matter(self, content):
        metadata = {}
        if content.startswith('---'):
            try:
                end_idx = content.index('---', 3)
                fm = content[3:end_idx].strip()
                metadata = yaml.safe_load(fm) or {}
                content = content[end_idx + 3:].strip()
            except Exception:
                pass
        return content, metadata


    # ------------------------
    #  HTML ➜ PDF
    # ------------------------
    def _html_to_pdf(self, html_content):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            html_path = f.name

        try:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as pdf_file:
                pdf_path = pdf_file.name

            document = weasyprint.HTML(filename=html_path)
            document.write_pdf(pdf_path)

            with open(pdf_path, 'rb') as f:
                import base64
                pdf_base64 = base64.b64encode(f.read()).decode('utf-8')

            return pdf_base64

        finally:
            os.unlink(html_path)
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# ------------------------------------------
#           TOOLS & AGENT (UNCHANGED)
# ------------------------------------------

generator = ContentGenerator()

@tool
def generate_pdf_document(markdown_content: str, output_file: str,
                          title: str = "Document",
                          author: str = "LearnAI",
                          date: str = "") -> str:

    try:
        pdf_base64 = generator.create_document(markdown_content, title, author, date)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        import base64
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(pdf_base64))

        return f"✅ Generated PDF at: {output_path.absolute()}"
    except Exception as e:
        return f"❌ Error generating PDF: {e}"


@tool
def generate_presentation_slides(markdown_content: str, output_file: str) -> str:

    try:
        pdf_base64 = generator.create_slides(markdown_content)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        import base64
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(pdf_base64))

        return f"✅ Slides saved to: {output_path.absolute()}"
    except Exception as e:
        return f"❌ Error generating slides: {e}"


@tool
def convert_markdown_file(input_file: str, output_file: str, format_type: str) -> str:

    try:
        path = Path(input_file)
        if not path.exists():
            return f"❌ Input not found: {input_file}"

        content = path.read_text(encoding='utf-8')

        if format_type.lower() == "slides":
            return generate_presentation_slides(content, output_file)

        metadata = {}
        if content.startswith('---'):
            try:
                end = content.index('---', 3)
                metadata = yaml.safe_load(content[3:end].strip()) or {}
            except:
                pass

        return generate_pdf_document(
            content,
            output_file,
            title=metadata.get('title', 'Document'),
            author=metadata.get('author', ''),
            date=metadata.get('date', '')
        )

    except Exception as e:
        return f"❌ Error: {e}"


class ContentGenerationConfig:
    """Configuration for the content generation agent."""

    agent_name: str = "Content Generator",
    description: str = "An AI agent that generates professional PDF documents and presentation slides from markdown content with LaTeX math support."
    system_prompt: str = AGENT_INSTRUCTIONS

class ContentGenerationAgent(Agent):

    def __init__(self):
        self.config = ContentGenerationConfig()
        self.agent = self._create_agent()
        self.current_user_id = None
        self.current_session_id = None

    def _create_agent(self) -> Agent:
        model = BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=False,
        )


        try:
            agent = Agent(
                name=self.config.agent_name,
                model=model,
                system_prompt=self.config.system_prompt,
                tools=[
                    generate_pdf_document,
                    generate_presentation_slides,
                    convert_markdown_file,
                ],
                description=self.config.description,
            )

            logger.info("✅ Agent created successfully with 3 tools")
        except Exception as e:
            logger.error(f"❌ Failed to create Agent/BedrockModel: {e}")
            raise

        return agent

    def chat(self, message: str, **kwargs) -> str:
        response = self.agent(message, **kwargs)
        return str(response)


def create_content_agent(
    user_id: Optional[str] = None,
    config: Optional[ContentGenerationConfig] = None
) -> ContentGenerationAgent:
    """
    Factory function to create a ContentGenerationAgent.

    Args:
        user_id: Optional user ID to set
        config: Optional configuration

    Returns:
        ContentGenerationAgent instance
    """
    agent = ContentGenerationAgent()
    if user_id:
        agent.current_user_id = user_id
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
