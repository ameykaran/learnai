"""Example orchestrator showing how to use the adapter and content agent.

This script demonstrates building an agent prompt from RAG results and calling
the content generation tools available in `agents/content_generation/agent.py`.
"""

from pathlib import Path
from agents.orchestrator.adapter import create_agent_prompt

# Import content agent factory
from agents.content_generation.agent import create_content_agent


def run_example():
    # Sample inputs
    user_query = "Create a short PDF report on conditional probability with examples."
    rag_results = [
        {'source': 'ncert_prob', 'text': 'Definition: Conditional probability...'},
        {'source': 'notes', 'text': 'Worked example: If a bag has 3 red, 2 blue...'}
    ]
    user_profile = {'name': 'Amey'}
    system_config = {'preferred_format': 'pdf', 'title': 'Conditional Probability - Short Report'}

    # Build prompt
    template = create_agent_prompt(user_query, user_profile, rag_results, system_config)

    print('Selected tool:', template['tool'])
    print('Metadata:', template['metadata'])

    # Create agent
    agent = create_content_agent()

    # For this example, we'll directly call the convert function via the tools
    # Save a small markdown file to feed the agent's convert function
    md = f"""---
title: {template['metadata']['title']}
author: {template['metadata']['author']}
---

{template['prompt']}
"""

    out_path = Path('output') / 'example_report.pdf'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Use the agent's convert_markdown_file tool by calling it through the agent
    # Note: the agent expects file paths; write the markdown to a temp file
    md_file = Path('output') / 'temp_content.md'
    md_file.write_text(md, encoding='utf-8')

    # Directly import the tool function and call it
    from agents.content_generation.agent import convert_markdown_file

    res = convert_markdown_file(str(md_file), str(out_path), format_type='pdf')
    print('\nResult:\n', res)


if __name__ == '__main__':
    run_example()
