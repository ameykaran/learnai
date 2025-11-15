#!/usr/bin/env python3
"""
Unified Markdown Converter - Single tool for PDF documents and presentation slides.
Usage: python3 converter.py input.md output.pdf --pdf
       python3 converter.py input.md output.pdf --slides
"""

import os
import sys
import tempfile
import argparse
from pathlib import Path

try:
    import markdown
    import weasyprint
    import yaml
    from jinja2 import Template
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please install: pip install markdown weasyprint pyyaml jinja2")
    sys.exit(1)


class UnifiedConverter:
    """Single converter for both PDF documents and presentation slides."""

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

    def convert(self, input_file, output_file, format_type):
        """Convert markdown file to PDF document or slides."""
        input_path = Path(input_file)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        content = input_path.read_text(encoding='utf-8')

        if format_type == "slides":
            return self._create_slides(content, output_file)
        else:  # pdf document
            return self._create_document(content, output_file)

    def _create_document(self, content, output_file):
        """Create PDF document."""
        # Parse front matter
        content, metadata = self._parse_front_matter(content)

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
        return self._html_to_pdf(html_doc, output_file)

    def _create_slides(self, content, output_file):
        """Create presentation slides."""
        # Remove YAML front matter if present
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
        return self._html_to_pdf(html_content, output_file)

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

    def _html_to_pdf(self, html_content, output_file):
        """Convert HTML to PDF using WeasyPrint."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name

        try:
            document = weasyprint.HTML(filename=temp_path)
            document.write_pdf(str(output_path))
            return str(output_path)
        finally:
            os.unlink(temp_path)

    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(
        description="Convert markdown to PDF documents or presentation slides",
        epilog="Examples:\n"
               "  python3 converter.py input.md output.pdf --pdf\n"
               "  python3 converter.py input.md slides.pdf --slides",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("output", help="Output PDF file")

    # Mutually exclusive group for format
    format_group = parser.add_mutually_exclusive_group(required=True)
    format_group.add_argument("--pdf", action="store_true", help="Create PDF document")
    format_group.add_argument("--slides", action="store_true", help="Create presentation slides")

    args = parser.parse_args()

    # Determine format
    format_type = "slides" if args.slides else "pdf"

    try:
        converter = UnifiedConverter()
        output_path = converter.convert(args.input, args.output, format_type)
        print(f"✅ Successfully converted '{args.input}' to '{output_path}' ({format_type})")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()