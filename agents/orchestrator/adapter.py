"""Adapter to convert user request + RAG chunks into content generation agent prompts.

Contract:
 - Inputs: topic (str), request_type ('pdf'|'slides'), rag_chunks (List[Dict]), user_profile (optional)
 - Output: dict with keys: prompt (str), metadata (dict), tool (str: 'pdf'|'slides')

This adapter bridges the orchestrator, RAG system, and content generation agent.
It formats RAG chunks (with structured metadata) into prompts that the content agent can use.
"""

from typing import List, Dict, Any, Optional
import textwrap
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.retrieval.backend.schema import Chunk, Metadata
from shared.models import UserProfile

logger = logging.getLogger(__name__)


def format_rag_chunks(chunks: List[Dict[str, Any]], max_chars: int = 8000) -> str:
    """
    Format RAG chunks into a structured markdown section.
    
    Each chunk has structured metadata including:
    - topics, chunk_type, difficulty_level, prerequisites
    
    Args:
        chunks: List of RAG chunk dictionaries
        max_chars: Maximum total characters (default 8000)
        
    Returns:
        Formatted markdown string with organized content
    """
    if not chunks:
        return "No content available."
    
    # Group chunks by type for better organization
    grouped = {
        'definition': [],
        'explanation': [],
        'example': [],
        'proof': [],
        'practice_problem': [],
        'worked_solution': [],
        'visualization': [],
        'analogy': [],
        'misconception': []
    }
    
    for chunk in chunks:
        chunk_type = chunk.get('chunk_type', 'explanation')
        if chunk_type in grouped:
            grouped[chunk_type].append(chunk)
    
    # Build formatted output
    sections = []
    total_chars = 0
    
    # Priority order for content types
    priority = ['definition', 'explanation', 'example', 'practice_problem', 
                'worked_solution', 'proof', 'visualization', 'analogy', 'misconception']
    
    for chunk_type in priority:
        items = grouped[chunk_type]
        if not items:
            continue
            
        # Format section header
        type_name = chunk_type.replace('_', ' ').title()
        section = f"\n## {type_name}s\n\n"
        
        for item in items:
            text = item.get('text', '')
            topics = item.get('topics', [])
            difficulty = item.get('difficulty_level', 'intermediate')
            prereqs = item.get('prerequisites', [])
            
            # Format chunk with metadata
            chunk_content = f"### {', '.join(topics) if topics else 'Content'}\n"
            chunk_content += f"*Difficulty: {difficulty}*\n\n"
            
            if prereqs:
                chunk_content += f"**Prerequisites:** {', '.join(prereqs)}\n\n"
            
            chunk_content += f"{text.strip()}\n\n"
            chunk_content += "---\n\n"
            
            # Check length
            if total_chars + len(section) + len(chunk_content) > max_chars:
                if total_chars == 0:  # Include at least one chunk
                    remaining = max_chars - total_chars
                    chunk_content = chunk_content[:remaining]
                    section += chunk_content
                    sections.append(section)
                break
            
            section += chunk_content
            total_chars += len(chunk_content)
        
        if section != f"\n## {type_name}s\n\n":
            sections.append(section)
        
        if total_chars >= max_chars:
            break
    
    return "\n".join(sections).strip()


def determine_content_type(request_type: str) -> str:
    """
    Determine the content generation tool to use.
    
    Args:
        request_type: Either 'pdf' or 'slides'
        
    Returns:
        Validated content type
    """
    if request_type.lower() in ('slides', 'slide', 'presentation', 'ppt'):
        return 'slides'
    elif request_type.lower() in ('pdf', 'document', 'doc', 'report'):
        return 'pdf'
    else:
        # Default to PDF
        return 'pdf'


def create_content_generation_request(
    topic: str,
    request_type: str,
    rag_chunks: List[Dict[str, Any]],
    user_profile: Optional[UserProfile] = None,
    num_slides: Optional[int] = None,
    include_exercises: bool = False,
    max_chars: int = 8000
) -> Dict[str, Any]:
    """
    Main adapter function to create content generation request.
    
    This is called by the orchestrator after retrieving RAG chunks.
    It formats everything into a prompt the content generation agent can use.
    
    Args:
        topic: The topic/title for the content
        request_type: 'pdf' or 'slides'
        rag_chunks: List of RAG chunk dictionaries with structured metadata
        user_profile: Optional UserProfile for personalization
        num_slides: Number of slides (for presentations, default 10)
        include_exercises: Whether to include practice problems
        max_chars: Maximum characters from RAG content
        
    Returns:
        dict with keys: prompt (str), metadata (dict), tool (str)
    """
    # Validate and normalize request type
    content_type = determine_content_type(request_type)
    
    # Format RAG chunks into structured content
    formatted_content = format_rag_chunks(rag_chunks, max_chars=max_chars)
    
    # Build metadata
    metadata = {
        'tool': content_type,
        'title': topic,
        'author': user_profile.user_id if user_profile else 'Student',
        'num_chunks': len(rag_chunks),
        'topics': list(set(
            topic for chunk in rag_chunks 
            for topic in chunk.get('topics', [])
        ))[:5]  # Top 5 unique topics
    }
    
    # Add user-specific metadata if available
    if user_profile:
        metadata['competence_level'] = user_profile.competence_level
        metadata['recommended_level'] = user_profile.recommended_starting_level
        metadata['learning_pace'] = user_profile.learning_pace
    
    # Build personalized prompt
    if content_type == 'slides':
        num_slides = num_slides or 10
        prompt = _create_slides_prompt(
            topic, formatted_content, num_slides, 
            include_exercises, user_profile
        )
    else:  # pdf
        prompt = _create_pdf_prompt(
            topic, formatted_content, 
            include_exercises, user_profile
        )
    
    return {
        'prompt': prompt,
        'metadata': metadata,
        'tool': content_type
    }


def _create_slides_prompt(
    topic: str,
    content: str,
    num_slides: int,
    include_exercises: bool,
    user_profile: Optional[UserProfile]
) -> str:
    """Create a prompt for slide generation."""
    
    # Personalization based on user level
    level_guidance = ""
    if user_profile:
        if user_profile.competence_level == "easy":
            level_guidance = """
- Use simple, clear language
- Include more examples and visual explanations
- Break complex concepts into smaller steps
- Add analogies to aid understanding
"""
        elif user_profile.competence_level == "difficult":
            level_guidance = """
- Use technical terminology appropriately
- Include advanced concepts and proofs
- Focus on deep understanding and connections
- Add challenging problems
"""
        else:  # medium
            level_guidance = """
- Balance theory and practice
- Include both intuitive and formal explanations
- Provide a mix of basic and intermediate problems
"""
    
    exercise_guidance = ""
    if include_exercises:
        exercise_guidance = """
Include practice problems:
- Mix of difficulty levels
- Step-by-step solutions
- Common mistakes to avoid
"""
    
    prompt = textwrap.dedent(f"""
    You are an expert educational content creator. Generate a {num_slides}-slide presentation on: {topic}

    **Target Audience:** {user_profile.competence_level if user_profile else 'General'} level students
    
    **Content Guidelines:**
    {level_guidance}
    {exercise_guidance}
    
    **Structure:**
    1. Title slide with topic
    2. Overview/outline slide
    3. Main content slides (definitions, explanations, examples)
    4. Summary slide
    5. References (if applicable)
    
    **Formatting:**
    - Use markdown for all content
    - Keep each slide focused on ONE key concept
    - Use bullet points for clarity
    - Include code blocks with ```language for technical content
    - Use > for important notes/callouts
    - Include mathematical notation where appropriate
    
    **Source Content:**
    Use the following retrieved educational content as your authoritative source.
    This content is organized by type (definitions, explanations, examples, etc.):
    
    {content}
    
    **Important:**
    - Stay true to the source content - don't make up information
    - If source content is insufficient, indicate which topics need more material
    - Adapt the difficulty level to the target audience
    - Make connections between concepts explicit
    
    Generate the {num_slides} slides now in markdown format.
    """).strip()
    
    return prompt


def _create_pdf_prompt(
    topic: str,
    content: str,
    include_exercises: bool,
    user_profile: Optional[UserProfile]
) -> str:
    """Create a prompt for PDF document generation."""
    
    # Personalization based on user level
    level_guidance = ""
    if user_profile:
        if user_profile.competence_level == "easy":
            level_guidance = """
- Use accessible language with clear definitions
- Include numerous worked examples
- Add visual aids and diagrams where possible
- Provide step-by-step explanations
"""
        elif user_profile.competence_level == "difficult":
            level_guidance = """
- Use precise mathematical/technical language
- Include formal proofs and derivations
- Add advanced topics and extensions
- Provide challenging exercises
"""
        else:  # medium
            level_guidance = """
- Balance intuitive and formal explanations
- Include both conceptual and procedural knowledge
- Provide varied examples and practice problems
"""
    
    exercise_section = ""
    if include_exercises:
        exercise_section = """
## Practice Problems
- Include 5-10 problems of varying difficulty
- Provide complete solutions
- Highlight common errors and misconceptions
"""
    
    prompt = textwrap.dedent(f"""
    You are an expert educational content creator. Generate a comprehensive PDF document on: {topic}

    **Target Audience:** {user_profile.competence_level if user_profile else 'General'} level students
    
    **Content Guidelines:**
    {level_guidance}
    
    **Document Structure:**
    # {topic}
    
    ## Introduction
    - Overview of the topic
    - Learning objectives
    - Prerequisites
    
    ## Main Content
    - Organized into logical sections
    - Definitions, theorems, and key concepts
    - Detailed explanations
    - Worked examples
    - Connections to other topics
    
    {exercise_section}
    
    ## Summary
    - Key takeaways
    - Further reading
    
    **Formatting Guidelines:**
    - Use markdown syntax throughout
    - Use # ## ### for section headers
    - Use **bold** for key terms
    - Use *italic* for emphasis
    - Use ``` for code blocks
    - Use > for important notes
    - Use tables for comparisons
    - Include mathematical notation where needed
    
    **Source Content:**
    Use the following retrieved educational content as your authoritative source.
    This content is organized by type and difficulty level:
    
    {content}
    
    **Important:**
    - Base all content on the provided source material
    - Don't fabricate examples or explanations
    - If source material is limited, note what's missing
    - Maintain academic rigor appropriate to the level
    - Make learning engaging and accessible
    
    Generate the complete PDF document now in markdown format.
    """).strip()
    
    return prompt


if __name__ == '__main__':
    # Simple manual test runner
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("Testing adapter with sample RAG chunks...")
    
    sample_chunks = [
        {
            'id': '1',
            'text': 'Conditional probability is the probability of an event occurring given that another event has already occurred. It is denoted as P(A|B) and calculated as P(A|B) = P(A ∩ B) / P(B).',
            'topics': ['conditional probability', 'probability theory'],
            'chunk_type': 'definition',
            'difficulty_level': 'basic',
            'prerequisites': ['basic probability'],
            'source_url': 'ncert_chapter_15'
        },
        {
            'id': '2',
            'text': 'Example: If a die is rolled and we know it shows an even number, what is the probability it is a 2? P(2|even) = P(2 ∩ even)/P(even) = (1/6)/(3/6) = 1/3.',
            'topics': ['conditional probability'],
            'chunk_type': 'example',
            'difficulty_level': 'basic',
            'prerequisites': ['basic probability'],
            'source_url': 'ncert_chapter_15'
        }
    ]
    
    # Test 1: Slides generation
    print("\n=== Test 1: Slides Generation ===")
    result = create_content_generation_request(
        topic="Conditional Probability",
        request_type="slides",
        rag_chunks=sample_chunks,
        num_slides=5,
        include_exercises=True
    )
    print(f"Tool: {result['tool']}")
    print(f"Metadata: {result['metadata']}")
    print(f"\nPrompt preview:\n{result['prompt'][:500]}...")
    
    # Test 2: PDF generation with user profile
    print("\n=== Test 2: PDF Generation with User Profile ===")
    from shared.models import UserProfile
    
    profile = UserProfile(
        user_id="test_user",
        session_id="test_session",
        competence_level="medium",
        ability_score=0.6,
        final_score=60.0,
        recommended_starting_level="medium"
    )
    
    result = create_content_generation_request(
        topic="Advanced Probability Concepts",
        request_type="pdf",
        rag_chunks=sample_chunks,
        user_profile=profile,
        include_exercises=True
    )
    print(f"Tool: {result['tool']}")
    print(f"Metadata: {result['metadata']}")
    print(f"\nPrompt preview:\n{result['prompt'][:500]}...")
    
    print("\n✅ Adapter tests complete!")
