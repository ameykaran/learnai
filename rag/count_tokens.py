"""
Metadata-Rich Chunk Extraction System with Token Tracking

Enhanced version that tracks input/output tokens for cost analysis and monitoring.
"""

import json
import hashlib
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict

import dspy
from dotenv import load_dotenv
from google import genai

from agents.retrieval.backend.schema import Chunk

load_dotenv()

# Configuration constants
MAX_RETRIES = 3
RETRY_DELAY = 60
MAX_WORKERS = 5
DEFAULT_CHUNK_SIZE = 5000
DEFAULT_OVERLAP = 500


@dataclass
class TokenUsage:
    """Track token usage across all API calls."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    api_calls: int = 0
    
    def add(self, prompt: int, completion: int):
        """Add tokens from a single API call."""
        self.prompt_tokens += prompt
        self.completion_tokens += completion
        self.total_tokens += (prompt + completion)
        self.api_calls += 1
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def __str__(self):
        return (f"TokenUsage(calls={self.api_calls}, "
                f"prompt={self.prompt_tokens:,}, "
                f"completion={self.completion_tokens:,}, "
                f"total={self.total_tokens:,})")


class ChunkExtractor(dspy.Signature):
    """DSPy signature for extracting structured metadata-rich chunks."""
    markdown: str = dspy.InputField(desc="OCR markdown text from a PDF segment.")
    source_url: str = dspy.InputField(desc="Source document identifier or URL.")
    source_type: str = dspy.InputField(desc="Type of source material (textbook, paper, etc.).")
    
    chunks: List[Chunk] = dspy.OutputField(
        desc="A list of structured chunks with metadata (topics, difficulty, prerequisites, etc.)."
    )


def count_tokens_genai(text: str, model: str = "gemini-2.5-flash") -> int:
    """
    Count tokens in text using Google GenAI client.
    
    Args:
        text: Text to count tokens for
        model: Model to use for tokenization
    
    Returns:
        Token count
    """
    try:
        client = genai.Client()
        result = client.models.count_tokens(model=model, contents=text)
        return result.total_tokens
    except Exception as e:
        print(f"⚠️ Token counting failed: {e}")
        # Fallback to rough estimate (1 token ≈ 4 chars for English)
        return len(text) // 4


def extract_token_usage_from_dspy(prediction) -> Tuple[int, int]:
    """
    Extract token usage from DSPy prediction object.
    
    DSPy stores the raw LLM response in prediction metadata.
    For Gemini, this includes usage_metadata.
    
    Args:
        prediction: DSPy Prediction object
    
    Returns:
        Tuple of (prompt_tokens, completion_tokens)
    """
    try:
        # Access DSPy's internal trace/history
        if hasattr(prediction, '_trace'):
            # DSPy stores raw API responses in trace
            trace = prediction._trace
            if trace and len(trace) > 0:
                last_call = trace[-1]
                if hasattr(last_call, 'usage_metadata'):
                    usage = last_call.usage_metadata
                    return (usage.prompt_token_count, 
                            usage.candidates_token_count)
        
        # Alternative: Check if lm_response is available
        if hasattr(prediction, 'lm_response'):
            response = prediction.lm_response
            if hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                return (usage.prompt_token_count,
                        usage.candidates_token_count)
        
        # Fallback: estimate from content
        print("⚠️ Could not extract exact token usage from DSPy response")
        return (0, 0)
        
    except Exception as e:
        print(f"⚠️ Error extracting token usage: {e}")
        return (0, 0)


def split_with_overlap(
    text: str, 
    max_chars: int = DEFAULT_CHUNK_SIZE, 
    overlap: int = DEFAULT_OVERLAP
) -> List[str]:
    """Split text into overlapping segments."""
    if len(text) <= max_chars:
        return [text]
    
    parts = []
    start = 0

    while start < len(text):
        end = min(start + max_chars, len(text))
        parts.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
        if start < 0:
            start = 0
    
    return parts


def deduplicate_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate chunks based on content hash."""
    seen_hashes = set()
    unique_chunks = []
    
    for chunk in chunks:
        text_hash = hashlib.sha256(
            chunk["text"].strip().encode("utf-8")
        ).hexdigest()
        
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
) -> Tuple[List[Dict[str, Any]], TokenUsage]:
    """
    Extract structured chunks with token usage tracking.
    
    Returns:
        Tuple of (chunks_list, token_usage)
    """
    segments = split_with_overlap(ocr_markdown, max_chars=chunk_size, overlap=overlap)
    print(f"🟢 Split document into {len(segments)} overlapping segments.")

    # Configure DSPy
    lm = dspy.LM(
        model="gemini/gemini-2.5-flash",
        api_key=gemini_api_key or "",
        max_tokens=chunk_size * 3,
        num_retries=MAX_RETRIES,
        temperature=temperature
    )
    dspy.configure(lm=lm)
    
    extractor = dspy.Predict(ChunkExtractor)

    # Track token usage
    token_usage = TokenUsage()
    all_chunks = []
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, segment in enumerate(segments, start=1):
            print(f"Submitting task {i}/{len(segments)}")
            future = executor.submit(
                extractor,
                markdown=segment,
                source_url=source_url,
                source_type=source_type
            )
            futures.append((future, segment))

        for future, segment in futures:
            try:
                result = future.result()
                extracted_chunks = result.chunks
                
                # Extract token usage from DSPy response
                prompt_tokens, completion_tokens = extract_token_usage_from_dspy(result)
                
                # If extraction failed, estimate from segment
                if prompt_tokens == 0:
                    prompt_tokens = count_tokens_genai(segment)
                    # Estimate completion tokens from response
                    if extracted_chunks:
                        response_text = json.dumps([c.model_dump() for c in extracted_chunks])
                        completion_tokens = count_tokens_genai(response_text)
                
                token_usage.add(prompt_tokens, completion_tokens)
                
                if extracted_chunks:
                    print(f"✅ Worker completed: {len(extracted_chunks)} chunks | "
                          f"Tokens: {prompt_tokens}→{completion_tokens}")
                    all_chunks.extend(extracted_chunks)
                else:
                    print(f"🟡 Worker returned no chunks | Tokens: {prompt_tokens}→{completion_tokens}")
                    
            except Exception as e:
                print(f"⚠️ Worker failed: {e}")

    all_chunk_dicts = [chunk.model_dump() for chunk in all_chunks]
    unique_chunks = deduplicate_chunks(all_chunk_dicts)
    
    print(f"\n✅ Extracted {len(unique_chunks)} unique chunks from {len(all_chunk_dicts)} total.")
    print(f"📊 {token_usage}")
    
    return unique_chunks, token_usage


def process_file(
    input_md_path: str,
    output_json_path: str,
    source_url: str,
    source_type: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    max_workers: int = MAX_WORKERS,
    save_token_stats: bool = True
) -> TokenUsage:
    """
    Process markdown file and save chunks with token statistics.
    
    Returns:
        TokenUsage object with statistics
    """
    print(f"📖 Processing file: {input_md_path}")
    
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

    chunks, token_usage = extract_metadata_chunks(
        ocr_markdown=ocr_text,
        source_url=source_url,
        source_type=source_type,
        chunk_size=chunk_size,
        overlap=overlap,
        max_workers=max_workers
    )

    # Prepare output with metadata
    output_data = {
        "metadata": {
            "source_url": source_url,
            "source_type": source_type,
            "total_chunks": len(chunks),
            "token_usage": token_usage.to_dict()
        },
        "chunks": chunks
    }

    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Saved {len(chunks)} chunks to {output_json_path}")
        
        # Optionally save token stats separately
        if save_token_stats:
            stats_path = output_json_path.replace('.json', '_token_stats.json')
            with open(stats_path, "w", encoding="utf-8") as f:
                json.dump(token_usage.to_dict(), f, indent=2)
            print(f"📊 Saved token statistics to {stats_path}")
            
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        raise
    
    return token_usage


def batch_process_files(
    file_configs: List[Dict[str, str]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP
) -> TokenUsage:
    """
    Process multiple files and return aggregate token usage.
    """
    print(f"🚀 Starting batch processing of {len(file_configs)} files...\n")
    
    total_usage = TokenUsage()
    
    for i, config in enumerate(file_configs, start=1):
        print(f"\n{'='*60}")
        print(f"Processing file {i}/{len(file_configs)}")
        print(f"{'='*60}")
        
        try:
            usage = process_file(
                input_md_path=config["input_md_path"],
                output_json_path=config["output_json_path"],
                source_url=config["source_url"],
                source_type=config["source_type"],
                chunk_size=chunk_size,
                overlap=overlap
            )
            total_usage.add(usage.prompt_tokens, usage.completion_tokens)
            total_usage.api_calls = usage.api_calls  # Keep call count accurate
            
        except Exception as e:
            print(f"❌ Failed to process {config['input_md_path']}: {e}")
            continue
    
    print(f"\n✅ Batch processing complete!")
    print(f"📊 Total {total_usage}")
    
    return total_usage


if __name__ == "__main__":
    # Single file processing with token tracking
    token_usage = process_file(
        input_md_path="../ncertFullChapter/probabilityTes1.md",
        output_json_path="extracted_chunks-test.json",
        source_url="class12_ncert_textbook.pdf",
        source_type="textbook"
    )
    
    print(f"\n{'='*60}")
    print("FINAL TOKEN USAGE SUMMARY")
    print(f"{'='*60}")
    print(f"Total API Calls: {token_usage.api_calls}")
    print(f"Input Tokens:    {token_usage.prompt_tokens:,}")
    print(f"Output Tokens:   {token_usage.completion_tokens:,}")
    print(f"Total Tokens:    {token_usage.total_tokens:,}")
    print(f"{'='*60}")