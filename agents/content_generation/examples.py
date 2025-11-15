#!/usr/bin/env python3
"""
Example usage of the Content Generation Strands Agent
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import create_content_agent, generate_pdf_document, generate_presentation_slides


markdown_content = r"""

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
