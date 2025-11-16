#!/usr/bin/env python3
"""
Example usage of the Content Generation Strands Agent
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import create_content_agent, generate_pdf_document, generate_presentation_slides

with open("./sample.md", "r") as f:
    markdown_content = f.read()

def example_1_simple_document():
    """Example 1: Generate a simple PDF document"""
    print("\n" + "="*60)
    print("Example 1: Generate Simple PDF Document")
    print("="*60)
    
#     markdown_content = """
# # Welcome to Content Generation

# This is a **simple example** of generating a PDF document using the Strands Agent.

# ## Features

# - Clean typography
# - Professional styling
# - Markdown support

# ## Code Example

# ```python
# def hello():
#     print("Hello, World!")
# ```

# ## Table Example

# | Feature | Status |
# |---------|--------|
# | PDF Generation | ✅ |
# | Slides | ✅ |
# | Markdown | ✅ |
# """
    
    result = generate_pdf_document(
        markdown_content=markdown_content,
        output_file="output/example_document.pdf",
        title="Example Document",
        author="Strands Agent",
        date="2024"
    )
    
    print(result)


def example_2_presentation_slides():
    """Example 2: Generate presentation slides"""
    print("\n" + "="*60)
    print("Example 2: Generate Presentation Slides")
    print("="*60)
    
    result = generate_presentation_slides(
        markdown_content=markdown_content,
        output_file="output/example_slides.pdf"
    )
    
    print(result)


def example_3_agent_interaction():
    """Example 3: Interactive agent usage"""
    print("\n" + "="*60)
    print("Example 3: Agent Interaction")
    print("="*60)
    
    agent = create_content_agent()
    
    # Example conversations
    queries = [
        "Create a PDF document titled 'Meeting Notes' with this content: # Meeting Summary\n\n## Attendees\n- Alice\n- Bob\n\n## Action Items\n- Review proposal\n- Schedule follow-up",
        
        "Generate presentation slides about Python with 3 slides covering: introduction, key features, and example code"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}:")
        print(f"  {query[:80]}...")
        print(f"\n🤖 Agent Response:")
        
        response = agent(query)
        print(f"  {response}")


def example_4_file_conversion():
    """Example 4: Convert existing markdown file"""
    print("\n" + "="*60)
    print("Example 4: File Conversion")
    print("="*60)
    
    # Create a sample markdown file
    sample_md = """
---
title: Technical Report
author: AI Assistant
date: 2024-01-15
---

# Executive Summary

This report demonstrates file conversion capabilities.

## Background

Markdown files can be easily converted to professional PDFs.

## Methodology

1. Read markdown file
2. Parse content
3. Generate PDF with styling

## Conclusion

The conversion process is seamless and produces high-quality output.
"""
    
    # Save sample file
    os.makedirs("output", exist_ok=True)
    with open("output/sample_report.md", "w") as f:
        f.write(sample_md)
    
    print("Created sample file: output/sample_report.md")
    
    # Use agent to convert
    agent = create_content_agent()
    response = agent("Convert output/sample_report.md to a PDF at output/converted_report.pdf")
    
    print(f"\n{response}")


def main():
    """Run all examples"""
    print("\n" + "🎨" * 30)
    print("Content Generation Strands Agent - Examples")
    print("🎨" * 30)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    try:
        # Run examples
        example_1_simple_document()
        example_2_presentation_slides()
        
        print("\n" + "="*60)
        print("✅ Basic examples completed!")
        print("="*60)
        
        # Optional: Run agent interaction examples
        print("\n⚠️  Agent interaction examples require a configured model provider.")
        print("   Set up AWS credentials for Bedrock or configure another provider.")
        
        response = input("\nRun agent interaction examples? (y/n): ").strip().lower()
        if response == 'y':
            example_3_agent_interaction()
            example_4_file_conversion()
        
        print("\n" + "="*60)
        print("🎉 All examples completed!")
        print("="*60)
        print("\nGenerated files:")
        print("  - output/example_document.pdf")
        print("  - output/example_slides.pdf")
        if response == 'y':
            print("  - output/sample_report.md")
            print("  - output/converted_report.pdf")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
