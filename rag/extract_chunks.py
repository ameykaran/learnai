"""
Metadata-Rich Chunk Extraction System using DSPy and Gemini

This module extracts structured, metadata-rich chunks from OCR markdown text using:
- DSPy framework for structured output generation
- Google Gemini 2.5 Flash for intelligent content parsing
- Parallel processing for efficient handling of large documents
- Automatic deduplication of overlapping content

The system splits large documents into overlapping segments, processes them in parallel,
and extracts structured chunks with rich metadata (topics, difficulty, prerequisites, etc.).
"""

import json
import hashlib
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

import dspy
from dotenv import load_dotenv

from schema import Chunk

# Load environment variables (API keys, etc.)
load_dotenv()

# Configuration constants
MAX_RETRIES = 3        # Number of retries for failed API calls
RETRY_DELAY = 60       # Delay between retries in seconds
MAX_WORKERS = 5        # Maximum parallel workers for chunk processing
DEFAULT_CHUNK_SIZE = 5000   # Characters per segment
DEFAULT_OVERLAP = 500       # Overlap between segments to preserve context


class ChunkExtractor(dspy.Signature):
    """
    DSPy signature for extracting structured metadata-rich chunks from OCR markdown.
    
    This signature defines the input-output schema for the LLM to extract educational
    content chunks with comprehensive metadata including topics, difficulty levels,
    prerequisites, and chunk types.
    
    Inputs:
        markdown: OCR-extracted markdown text from a PDF segment
        source_url: URL or identifier of the source document
        source_type: Type of source (e.g., "textbook", "paper", "lecture_notes")
    
    Outputs:
        chunks: List of Chunk objects with structured metadata
    """
    markdown: str = dspy.InputField(desc="OCR markdown text from a PDF segment.")
    source_url: str = dspy.InputField(desc="Source document identifier or URL.")
    source_type: str = dspy.InputField(desc="Type of source material (textbook, paper, etc.).")
    
    # DSPy automatically generates a prompt to produce a JSON list of Chunk objects
    chunks: List[Chunk] = dspy.OutputField(
        desc="A list of structured chunks with metadata (topics, difficulty, prerequisites, etc.)."
    )


def split_with_overlap(
    text: str, 
    max_chars: int = DEFAULT_CHUNK_SIZE, 
    overlap: int = DEFAULT_OVERLAP
) -> List[str]:
    """
    Split text into overlapping segments for parallel processing.
    
    This function creates overlapping segments to ensure context is preserved
    across chunk boundaries. The overlap helps the LLM maintain continuity
    when processing long documents.
    
    Args:
        text: Input text to split
        max_chars: Maximum characters per segment (default: 5000)
        overlap: Number of overlapping characters between segments (default: 500)
    
    Returns:
        List of text segments with overlap
    
    Example:
        >>> text = "A" * 10000
        >>> segments = split_with_overlap(text, max_chars=5000, overlap=500)
        >>> len(segments)
        3
        >>> len(segments[0])
        5000
    """
    # Handle short texts that don't need splitting
    if len(text) <= max_chars:
        return [text]
    
    parts = []
    start = 0

    while start < len(text):
        # Calculate end position for this segment
        end = min(start + max_chars, len(text))
        parts.append(text[start:end])

        # Break if we've reached the end
        if end == len(text):
            break
        
        # Move start position back by overlap amount for next segment
        start = end - overlap
        
        # Prevent negative indexing
        if start < 0:
            start = 0
    
    return parts


def deduplicate_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate chunks based on content hash.
    
    When processing overlapping segments, the same content may be extracted
    multiple times. This function deduplicates based on a SHA-256 hash of
    the chunk text.
    
    Args:
        chunks: List of chunk dictionaries with 'text' field
    
    Returns:
        List of unique chunks (first occurrence preserved)
    
    Example:
        >>> chunks = [{"text": "Hello"}, {"text": "Hello"}, {"text": "World"}]
        >>> unique = deduplicate_chunks(chunks)
        >>> len(unique)
        2
    """
    seen_hashes = set()
    unique_chunks = []
    
    for chunk in chunks:
        # Create hash from stripped text content
        text_hash = hashlib.sha256(
            chunk["text"].strip().encode("utf-8")
        ).hexdigest()
        
        # Only add if we haven't seen this content before
        if text_hash not in seen_hashes:
            seen_hashes.add(text_hash)
            unique_chunks.append(chunk)
    
    return unique_chunks


def extract_metadata_chunks(
    ocr_markdown: str,
    source_url: str,
    source_type: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    max_workers: int = MAX_WORKERS,
    gemini_api_key: str = None,
    temperature: float = 0.2
) -> List[Dict[str, Any]]:
    """
    Extract structured metadata-rich chunks from markdown text using parallel processing.
    
    This function:
    1. Splits the document into overlapping segments
    2. Processes segments in parallel using Gemini via DSPy
    3. Extracts structured chunks with metadata from each segment
    4. Deduplicates chunks across all segments
    
    Args:
        ocr_markdown: OCR-extracted markdown text from PDF
        source_url: Source document identifier or URL
        source_type: Type of source (textbook, paper, lecture_notes, etc.)
        chunk_size: Maximum characters per processing segment (default: 5000)
        overlap: Overlap between segments in characters (default: 500)
        max_workers: Maximum parallel workers (default: 5)
        gemini_api_key: Google Gemini API key (optional, uses env if not provided)
        temperature: LLM temperature for generation (default: 0.2 for consistency)
    
    Returns:
        List of deduplicated chunk dictionaries with metadata
    
    Example:
        >>> chunks = extract_metadata_chunks(
        ...     ocr_markdown=long_text,
        ...     source_url="textbook.pdf",
        ...     source_type="textbook"
        ... )
        🟢 Split document into 5 overlapping segments for DSPy-based processing.
        Submitting task 1/5
        ...
        ✅ Extracted 45 unique structured chunks from 52 total.
    """
    # Split document into manageable segments
    segments = split_with_overlap(ocr_markdown, max_chars=chunk_size, overlap=overlap)
    print(f"🟢 Split document into {len(segments)} overlapping segments for DSPy-based processing.")

    # Configure DSPy with Gemini LLM
    lm = dspy.LM(
        model="gemini/gemini-2.5-flash",
        api_key=gemini_api_key or "",  # Uses env variable if not provided
        max_tokens=chunk_size * 3,     # Allow extra tokens for structured output
        num_retries=MAX_RETRIES,
        temperature=temperature
    )
    dspy.configure(lm=lm)
    dspy.settings.configure(track_usage=True)

    
    # Initialize the chunk extractor
    extractor = dspy.Predict(ChunkExtractor)

    # Process segments in parallel
    all_chunks = []
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all extraction tasks
        for i, segment in enumerate(segments, start=1):
            print(f"Submitting task {i}/{len(segments)}")
            future = executor.submit(
                extractor,
                markdown=segment,
                source_url=source_url,
                source_type=source_type
            )
            futures.append(future)

        # Collect results as they complete
        for future in as_completed(futures):
            try:
                # Get the DSPy Prediction object
                result = future.result()
                
                # Extract the chunks from the prediction
                extracted_chunks = result.chunks
                
                if extracted_chunks:
                    print(f"✅ DSPy worker completed. Received {len(extracted_chunks)} chunks.")
                    all_chunks.extend(extracted_chunks)
                else:
                    print("🟡 DSPy worker returned no chunks.")
                    
            except Exception as e:
                print(f"⚠️ DSPy worker failed: {e}")

    # Convert Pydantic objects to dictionaries for JSON serialization
    all_chunk_dicts = [chunk.model_dump() for chunk in all_chunks]
    
    # Remove duplicates from overlapping segments
    unique_chunks = deduplicate_chunks(all_chunk_dicts)
    
    print(f"\n✅ Extracted {len(unique_chunks)} unique structured chunks from {len(all_chunk_dicts)} total.")
    return unique_chunks


def process_file(
    input_md_path: str,
    output_json_path: str,
    source_url: str,
    source_type: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    max_workers: int = MAX_WORKERS
) -> None:
    """
    Process a markdown file to extract structured chunks and save to JSON.
    
    This is the main entry point for batch processing. It loads a markdown file,
    extracts structured chunks with metadata, and saves the results as JSON.
    
    Args:
        input_md_path: Path to input markdown file (OCR output)
        output_json_path: Path to save extracted chunks as JSON
        source_url: Source document identifier
        source_type: Type of source material
        chunk_size: Characters per processing segment (default: 5000)
        overlap: Overlap between segments (default: 500)
        max_workers: Maximum parallel workers (default: 5)
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        IOError: If output file cannot be written
    
    Example:
        >>> process_file(
        ...     input_md_path="textbook.md",
        ...     output_json_path="chunks.json",
        ...     source_url="textbook.pdf",
        ...     source_type="textbook"
        ... )
        Loaded 125000 characters from markdown file.
        🟢 Split document into 25 overlapping segments for DSPy-based processing.
        ...
        ✅ Saved 150 extracted chunks to chunks.json
    """
    print(f"📖 Processing file: {input_md_path}")
    
    # Load markdown file
    try:
        with open(input_md_path, "r", encoding="utf-8") as f:
            ocr_text = f.read()
        print(f"✅ Loaded {len(ocr_text):,} characters from markdown file.")
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_md_path}")
        raise
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        raise

    # Extract chunks
    chunks = extract_metadata_chunks(
        ocr_markdown=ocr_text,
        source_url=source_url,
        source_type=source_type,
        chunk_size=chunk_size,
        overlap=overlap,
        max_workers=max_workers
    )

    # Save to JSON
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Saved {len(chunks)} extracted chunks to {output_json_path}")
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        raise


def batch_process_files(
    file_configs: List[Dict[str, str]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP
) -> None:
    """
    Process multiple files in batch.
    
    Args:
        file_configs: List of dictionaries with keys:
            - input_md_path: Path to markdown file
            - output_json_path: Path for output JSON
            - source_url: Source identifier
            - source_type: Source type
        chunk_size: Characters per segment
        overlap: Overlap between segments
    
    Example:
        >>> configs = [
        ...     {
        ...         "input_md_path": "chapter1.md",
        ...         "output_json_path": "chapter1_chunks.json",
        ...         "source_url": "textbook_ch1.pdf",
        ...         "source_type": "textbook"
        ...     },
        ...     {...}
        ... ]
        >>> batch_process_files(configs)
    """
    print(f"🚀 Starting batch processing of {len(file_configs)} files...\n")
    
    for i, config in enumerate(file_configs, start=1):
        print(f"\n{'='*60}")
        print(f"Processing file {i}/{len(file_configs)}")
        print(f"{'='*60}")
        
        try:
            process_file(
                input_md_path=config["input_md_path"],
                output_json_path=config["output_json_path"],
                source_url=config["source_url"],
                source_type=config["source_type"],
                chunk_size=chunk_size,
                overlap=overlap
            )
        except Exception as e:
            print(f"❌ Failed to process {config['input_md_path']}: {e}")
            continue
    
    print(f"\n✅ Batch processing complete!")


# --- Main Execution ---

if __name__ == "__main__":
    # Single file processing example
    process_file(
        input_md_path="../data/probabilityncert.md",
        output_json_path="extracted_chunks.json",
        source_url="class12_ncert_textbook.pdf",
        source_type="textbook"
    )
    
    # Batch processing example (commented out)
    # batch_process_files([
    #     {
    #         "input_md_path": "chapter1.md",
    #         "output_json_path": "chapter1_chunks.json",
    #         "source_url": "textbook_ch1.pdf",
    #         "source_type": "textbook"
    #     },
    #     {
    #         "input_md_path": "chapter2.md",
    #         "output_json_path": "chapter2_chunks.json",
    #         "source_url": "textbook_ch2.pdf",
    #         "source_type": "textbook"
    #     }
    # ])