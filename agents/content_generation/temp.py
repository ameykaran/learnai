#!/usr/bin/env python3
"""
Robust Markdown -> KaTeX (server-side via Node) -> WeasyPrint PDF pipeline
Writes debug.html (open in browser to inspect) and output.pdf.

Requirements:
- Python packages: markdown, weasyprint
    pip install markdown weasyprint
- Node.js installed (node must be on PATH)
- katex installed in node (locally or globally):
    npm install katex
  or globally:
    npm install -g katex
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from weasyprint import HTML

# -------------------------
# Config / sample markdown
# -------------------------

MARKDOWN = r"""

## 1. Retrieved Content

### 1.1 Definitions
**Conditional Probability**: If E and F are two events associated with the same sample space of a random experiment, the conditional probability of event E given that F has occurred is:

$$P(E|F) = \frac{P(E \cap F)}{P(F)}$$

provided $P(F) \neq 0$

### 1.2 Explanations
Conditional probability addresses how the occurrence of one event affects the probability of another event. When we have two events from the same sample space, knowing that one event has occurred can change our calculation of the probability of the second event.

### 1.3 Examples
**Three Coins Example**: Consider tossing three fair coins with sample space:
$S = \{HHH, HHT, HTH, THH, HTT, THT, TTH, TTT\}$

Let:
- E = "at least two heads appear" = $\{HHH, HHT, HTH, THH\}$
- F = "first coin shows tail" = $\{THH, THT, TTH, TTT\}$

Then:
- $P(E) = \frac{4}{8} = \frac{1}{2}$
- $P(F) = \frac{4}{8} = \frac{1}{2}$
- $E \cap F = \{THH\}$, so $P(E \cap F) = \frac{1}{8}$

Therefore: $P(E|F) = \frac{P(E \cap F)}{P(F)} = \frac{\frac{1}{8}}{\frac{1}{2}} = \frac{1}{4}$

### 1.4 Proofs

### 1.5 Visualizations

### 1.6 Practice Problems
**Family with Two Children**: Assume each child is equally likely to be a boy or girl. If a family has two children, what is the conditional probability that both are girls given that:
(i) the youngest is a girl
(ii) at least one is a girl

### 1.7 Worked Solutions
**Basic Calculation**: If $P(A) = \frac{7}{13}$, $P(B) = \frac{9}{13}$, and $P(A \cap B) = \frac{4}{13}$, then:
$$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{\frac{4}{13}}{\frac{9}{13}} = \frac{4}{9}$$

**Urn Problem**: An urn contains 10 black and 5 white balls. Drawing two balls without replacement:
- $P(\text{first black}) = \frac{10}{15}$
- $P(\text{second black | first black}) = \frac{9}{14}$
- $P(\text{both black}) = \frac{10}{15} \times \frac{9}{14} = \frac{3}{7}$

### 1.8 Analogies

### 1.9 Misconceptions

## 2. Expert Explanation

Conditional probability is one of the most important concepts in probability theory. It measures the probability of an event occurring given that another event has already occurred.

**Key Intuition**: When we know that event F has happened, we essentially "shrink" our sample space to only include outcomes where F occurs. Within this reduced sample space, we then calculate the probability of event E.

**The Formula Breakdown**:
- $P(E \cap F)$ = probability that both E and F occur
- $P(F)$ = probability that F occurs (our "given" condition)
- The division gives us the proportion of F-outcomes that also satisfy E

**Why P(F) ≠ 0?**: We need this condition because we can't condition on an impossible event. If F never happens, the concept of "given F has occurred" is meaningless.

## 3. Extensions

**Real-World Application**: Consider medical testing:
- E = "person has disease"
- F = "test is positive"
- $P(E|F)$ = probability person has disease given positive test

This is different from $P(F|E)$ = probability of positive test given disease!

**Connection to Independence**: Two events E and F are independent if and only if $P(E|F) = P(E)$. This means knowing F occurred doesn't change the probability of E.

## 4. Next Steps

To deepen your understanding:
1. Practice calculating conditional probabilities with different examples
2. Explore Bayes' theorem, which uses conditional probability
3. Study the multiplication rule: $P(E \cap F) = P(E|F) \times P(F)$
4. Learn about the law of total probability
5. Apply conditional probability to real-world scenarios like medical diagnosis, quality control, or weather prediction
"""



OUT_HTML = Path("debug.html").resolve()
OUT_PDF = Path("output.pdf").resolve()

# -------------------------
# Helpers
# -------------------------
def check_node_and_katex():
    """Return tuple (ok:bool, message:str). Checks node and katex availability."""
    node_path = shutil.which("node")
    if not node_path:
        return False, "Node.js not found on PATH. Install Node (https://nodejs.org/) and ensure `node` is on PATH."

    # Run a short node snippet to require('katex')
    cmd = [
        "node",
        "-e",
        "try{require('katex'); console.log('__KATEX_OK__');}catch(e){console.error('KATEX_ERR:'+e.message); process.exit(2)}",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0 and "__KATEX_OK__" in proc.stdout:
        return True, "node and katex available"
    else:
        # If katex not found, show stderr
        stderr = proc.stderr.strip() or proc.stdout.strip()
        msg = "KaTeX not available to Node. Install with `npm install katex` in your project or `npm install -g katex`.\nNode stderr:\n" + stderr
        return False, msg

def convert_dollars_to_brackets(text: str) -> str:
    ESC = "__ESC__DOLLAR__"
    text = text.replace(r"\$", ESC)
    # $$...$$ -> \[...\]
    text = re.sub(r"\$\$(.+?)\$\$", lambda m: f"\\\\[{m.group(1)}\\\\]", text, flags=re.DOTALL)
    # $...$ -> \(...\)
    text = re.sub(r"(?<!\$)\$(.+?)(?<!\$)\$(?!\$)", lambda m: f"\\\\({m.group(1)}\\\\)", text, flags=re.DOTALL)
    return text.replace(ESC, r"\$")

# Node renderer will be written to a temp file
NODE_RENDERER_JS = r"""
// node katex renderer: reads latex from stdin, arg[2] = "display"|"inline"
const fs = require('fs');
const katex = require('katex');
const input = fs.readFileSync(0, 'utf8');
const mode = process.argv[2] === 'display';
try {
  const out = katex.renderToString(input, { displayMode: mode, throwOnError: false, strict: false });
  process.stdout.write(out);
} catch (err) {
  // Output a JSON-like error wrapper so Python can surface it
  process.stdout.write(JSON.stringify({__katex_error__: true, message: String(err && err.message || err)}));
  process.exit(1);
}
"""

def render_with_node_katex(latex: str, display: bool, renderer_path: Path):
    """Run node renderer with latex on stdin. Returns tuple (ok:bool, output_html_or_error:str)."""
    mode = "display" if display else "inline"
    try:
        proc = subprocess.run(
            ["node", str(renderer_path), mode],
            input=latex,
            text=True,
            capture_output=True,
            timeout=15,
        )
    except FileNotFoundError:
        return False, "node executable not found"
    except subprocess.TimeoutExpired:
        return False, "node renderer timed out"

    if proc.returncode == 0:
        return True, proc.stdout
    else:
        # try to parse JSON error if produced
        out = proc.stdout.strip()
        err = proc.stderr.strip()
        msg = out or err or f"node process failed with returncode {proc.returncode}"
        return False, msg

# -------------------------
# Main pipeline
# -------------------------
def main():
    ok, msg = check_node_and_katex()
    if not ok:
        print("Environment check failed:\n", msg, file=sys.stderr)
        # Still proceed to create debug HTML that shows the problem
    else:
        print("Environment ok:", msg)

    # Create node renderer temporary file (kept in cwd so node can require local katex)
    tmp_dir = Path.cwd() / "_katex_node"
    tmp_dir.mkdir(exist_ok=True)
    renderer_path = tmp_dir / "katex_renderer.js"
    renderer_path.write_text(NODE_RENDERER_JS)
    print("Wrote node renderer to:", renderer_path)

    # Step 1: convert dollar syntax
    md_conv = convert_dollars_to_brackets(MARKDOWN)

    # Step 2: Markdown -> HTML
    html_body = markdown.markdown(md_conv, extensions=["fenced_code", "tables"])

    # Step 3: replace math \
    # Patterns: match \[ ... \] and \( ... \) in the HTML
    # Use non-greedy DOTALL to capture across lines
    errors = []

    def repl_display(m):
        inner = m.group(1)
        ok2, out = render_with_node_katex(inner, True, renderer_path)
        if not ok2:
            errors.append(("display", inner, out))
            # show the original latex inside a <pre> for debugging
            escaped = inner.replace("<", "&lt;").replace(">", "&gt;")
            return f'<pre class="katex-fallback error">KaTeX render error: {out}\n\n{escaped}</pre>'
        return f'<div class="katex-display">{out}</div>'

    html_body = re.sub(r"\\\[(.+?)\\\]", repl_display, html_body, flags=re.DOTALL)

    def repl_inline(m):
        inner = m.group(1)
        ok2, out = render_with_node_katex(inner, False, renderer_path)
        if not ok2:
            errors.append(("inline", inner, out))
            escaped = inner.replace("<", "&lt;").replace(">", "&gt;")
            return f'<code class="katex-fallback error">KaTeX render error: {out} — latex: {escaped}</code>'
        return out

    html_body = re.sub(r"\\\((.+?)\\\)", repl_inline, html_body, flags=re.DOTALL)

    # Step 4: final HTML with katex CSS and diagnostics
    katex_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css">'
    diagnostic_html = ""
    if errors:
        diagnostic_html += "<div class='diagnostic'><h2>KaTeX render errors</h2><ul>"
        for typ, latex, err in errors:
            diag = f"<li><strong>{typ}</strong>: error: <pre>{err}</pre><details><summary>latex</summary><pre>{latex.replace('<','&lt;')}</pre></details></li>"
            diagnostic_html += diag
        diagnostic_html += "</ul></div>"

    html_full = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
{katex_css}
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 2rem; line-height:1.45; }}
.katex-display {{ margin: 1em 0; }}
.katex-fallback.error {{ color: #b33; background: #fee; padding: 0.5em; display: block; }}
.diagnostic {{ border: 1px solid #f88; background:#fff6f6; padding: 1em; margin-bottom:1em; }}
pre {{ white-space: pre-wrap; word-break: break-word; }}
</style>
</head>
<body>
{diagnostic_html}
{html_body}
</body>
</html>
"""

    OUT_HTML.write_text(html_full, encoding="utf8")
    print("Wrote debug HTML to:", OUT_HTML)

    # Step 5: write PDF using WeasyPrint (if katex rendering succeeded at least somewhat)
    try:
        HTML(string=html_full).write_pdf(str(OUT_PDF))
        print("Wrote PDF to:", OUT_PDF)
    except Exception as e:
        print("WeasyPrint failed:", e, file=sys.stderr)
        print("You can open debug.html in a browser to inspect the HTML output and any KaTeX errors.")

if __name__ == "__main__":
    main()
