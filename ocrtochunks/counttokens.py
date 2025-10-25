"""
images_to_structured_json_gemini_rest_with_token_counting.py

Enhanced version with token usage tracking per image and total cost calculation.

Key additions:
- Token counting using response metadata from Gemini API
- Per-image token tracking
- Total token usage and cost calculation
- Summary report with cost breakdown
"""

import os
import base64
import json
import time
from typing import List, Dict, Any, Optional
import requests
from PIL import Image


# Optional: dspy schema import (if installed)
try:
    import dspy
    from dspy import Document, Field, List as DList
    DSPY_AVAILABLE = True
except Exception:
    DSPY_AVAILABLE = False

# -------------------------
# Config
# -------------------------
GEMINI_REST_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
API_KEY = os.environ.get("GEMINI_API_KEY")  # must be set in environment
IMAGES_FOLDER = "output_images_Test1"   # folder with page_1.png etc
OUTPUT_JSON_PATH = "tokencountsdense/combined_structured.json"
RAW_OUTPUT_DIR = "tokencountsdense/raw_model_outputs"
STATS_OUTPUT_PATH = "tokencountsdense/token_usage_stats.json"  # NEW: Token statistics
REQUEST_SLEEP = 0.15  # small throttle (seconds) between requests to avoid burst limits

# GEMINI_REST_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
# API_KEY = os.environ.get("GEMINI_API_KEY")  # must be set in environment
# IMAGES_FOLDER = "output_images"   # folder with page_1.png etc
# OUTPUT_JSON_PATH = "tokencounts/combined_structured.json"
# RAW_OUTPUT_DIR = "tokencounts/raw_model_outputs"
# REQUEST_SLEEP = 0.15  # small throttle (seconds) between requests to avoid burst limits

# Pricing for Gemini 2.5 Flash (as of Oct 2024 - verify current pricing)
# https://ai.google.dev/pricing
PRICE_PER_1M_INPUT_TOKENS = 0.075  # $0.075 per 1M input tokens
PRICE_PER_1M_OUTPUT_TOKENS = 0.30  # $0.30 per 1M output tokens

# Allowed values for fields (lowercase)
ALLOWED_CHUNK_TYPES = {
    "definition",
    "example",
    "explanation",
    "proof",
    "visualization",
    "practice_problem",
    "worked_solution",
    "analogy",
    "misconception",
}
ALLOWED_DIFFICULTY = {"basic", "intermediate", "advanced"}

# Ensure API key
if not API_KEY:
    raise SystemExit("Please set GEMINI_API_KEY environment variable before running.")


# -------------------------
# Token Usage Tracking
# -------------------------
class TokenUsageTracker:
    """Track token usage across all API calls"""
    
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.per_image_stats = []
    
    def add_usage(self, filename: str, input_tokens: int, output_tokens: int, 
                  chunks_extracted: int = 0):
        """Record token usage for a single image"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        self.per_image_stats.append({
            "filename": filename,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "chunks_extracted": chunks_extracted,
            "input_cost_usd": (input_tokens / 1_000_000) * PRICE_PER_1M_INPUT_TOKENS,
            "output_cost_usd": (output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT_TOKENS,
        })
    
    def get_total_cost(self):
        """Calculate total cost in USD"""
        input_cost = (self.total_input_tokens / 1_000_000) * PRICE_PER_1M_INPUT_TOKENS
        output_cost = (self.total_output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT_TOKENS
        return input_cost + output_cost
    
    def get_summary(self):
        """Get summary statistics"""
        total_tokens = self.total_input_tokens + self.total_output_tokens
        input_cost = (self.total_input_tokens / 1_000_000) * PRICE_PER_1M_INPUT_TOKENS
        output_cost = (self.total_output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT_TOKENS
        total_cost = input_cost + output_cost
        
        return {
            "total_images_processed": len(self.per_image_stats),
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": total_tokens,
            "input_cost_usd": round(input_cost, 4),
            "output_cost_usd": round(output_cost, 4),
            "total_cost_usd": round(total_cost, 4),
            "average_tokens_per_image": round(total_tokens / len(self.per_image_stats)) if self.per_image_stats else 0,
            "average_cost_per_image_usd": round(total_cost / len(self.per_image_stats), 4) if self.per_image_stats else 0,
            "per_image_stats": self.per_image_stats,
            "pricing_info": {
                "input_token_price_per_1m": PRICE_PER_1M_INPUT_TOKENS,
                "output_token_price_per_1m": PRICE_PER_1M_OUTPUT_TOKENS,
                "note": "Verify current pricing at https://ai.google.dev/pricing"
            }
        }
    
    def print_summary(self):
        """Print a human-readable summary"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("TOKEN USAGE SUMMARY")
        print("="*60)
        print(f"Total Images Processed: {summary['total_images_processed']}")
        print(f"Total Input Tokens:     {summary['total_input_tokens']:,}")
        print(f"Total Output Tokens:    {summary['total_output_tokens']:,}")
        print(f"Total Tokens:           {summary['total_tokens']:,}")
        print("-"*60)
        print(f"Input Cost:             ${summary['input_cost_usd']:.4f}")
        print(f"Output Cost:            ${summary['output_cost_usd']:.4f}")
        print(f"TOTAL COST:             ${summary['total_cost_usd']:.4f}")
        print("-"*60)
        print(f"Average Tokens/Image:   {summary['average_tokens_per_image']:,}")
        print(f"Average Cost/Image:     ${summary['average_cost_per_image_usd']:.4f}")
        print("="*60)
        
        # Print top 5 most expensive images
        if self.per_image_stats:
            sorted_stats = sorted(self.per_image_stats, 
                                 key=lambda x: x['total_tokens'], 
                                 reverse=True)[:5]
            print("\nTop 5 Most Token-Intensive Images:")
            print("-"*60)
            for i, stat in enumerate(sorted_stats, 1):
                total_cost = stat['input_cost_usd'] + stat['output_cost_usd']
                print(f"{i}. {stat['filename']}")
                print(f"   Tokens: {stat['total_tokens']:,} "
                      f"(in: {stat['input_tokens']:,}, out: {stat['output_tokens']:,})")
                print(f"   Cost: ${total_cost:.4f}, Chunks: {stat['chunks_extracted']}")


# Initialize global tracker
token_tracker = TokenUsageTracker()


# -------------------------
# Optional DSPy schema (best-effort)
# -------------------------
if DSPY_AVAILABLE:
    try:
        class Metadata(Document):
            source_url: str = Field(str)
            source_type: str = Field(str)
            topics: List[str] = Field(DList(str))
            subtopics: List[str] = Field(DList(str))
            chunk_type: Optional[str] = Field((str, type(None)))
            difficulty_level: Optional[str] = Field((str, type(None)))
            prerequisites: List[str] = Field(DList(str))

        class PageExtract(Document):
            text: Optional[str] = Field((str, type(None)))
            page_number: Optional[int] = Field((int, type(None)))
            metadata: Optional[Metadata] = Field((Metadata, type(None)))
    except Exception:
        # If dspy API differs, fall back to simple path (we still won't crash)
        DSPY_AVAILABLE = False


def build_prompt_for_chunks(filename: str, page_number: int) -> str:
    """
    Strict prompt instructing Gemini to:
    - OCR the page and split it into atomic chunks (definition/example/...)
    - Render all math as LaTeX ($...$ / $$...$$)
    - Return EXACTLY one JSON ARRAY of objects (no commentary)
    """
    prompt = rf"""
You are an OCR + semantic chunker specialized for math textbooks (probability).

Input: an image of a textbook page (filename: "{filename}", page_number: {page_number}).
Task:
  1) Perform OCR on the page. Render all mathematical expressions as LaTeX:
     - Use inline math $...$ for inline expressions and $$...$$ for display equations.
     - Keep LaTeX faithful to the original, do not invent formulas.
  2) Split the page into atomic chunks, where each chunk is a single coherent item such as:
     - a definition,
     - an example,
     - an explanation (paragraph),
     - a proof,
     - a visualization caption/table/image description,
     - a practice_problem,
     - a worked_solution,
     - an analogy,
     - a misconception,
     - or any short self-contained text block (e.g., theorem statement, lemma).
     Do NOT produce a single giant chunk for the whole page. Prefer more granular chunks; if in doubt, split a long paragraph into multiple explanation chunks around topic shifts.
  3) For each chunk produce one object with this exact schema (use null for missing fields):

{{
  "text": <string or null>,
  "page_number": <int>,
  "chunk_index": <int>,
  "chunk_bbox": null,
  "metadata": {{
    "source_url": <string>,
    "source_type": <string>,
    "topics": <list of strings or null>,
    "subtopics": <list of strings or null>,
    "chunk_type": <string or null>,
    "difficulty_level": <string or null>,
    "prerequisites": <list of strings or null>
  }}
}}

Notes / constraints:
- Return EXACTLY one JSON ARRAY (e.g., [ {{...}}, {{...}}, ... ]) and nothing else.
- Use null for any field you cannot determine. Do not use "None" or other tokens.
- source_url should be the filename string (e.g., "{filename}"); source_type should be "image".
- chunk_type MUST be one of:
  ["definition","example","explanation","proof","visualization","practice_problem","worked_solution","analogy","misconception"] or null.
- difficulty_level MUST be one of ["basic","intermediate","advanced"] or null.
- Keep extracted text faithful; include LaTeX for math, e.g. $P(A \\mid B) = \\frac{{P(A \\cap B)}}{{P(B)}}$.
- For tables/images: produce a chunk with chunk_type "visualization" and put caption/description in text; set chunk_bbox to null if you cannot determine bounding box.

Return only the JSON array — no commentary, no explanations, no surrounding backticks.
"""
    return prompt.strip()

def call_gemini_rest(image_b64: str, mime_type: str, prompt_text: str) -> tuple[str, int, int]:
    """
    Call Gemini REST API and return (response_text, input_tokens, output_tokens)
    
    Returns:
        tuple: (response_text, input_token_count, output_token_count)
    """
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }

    # Build body according to the image-understanding REST example:
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_b64
                        }
                    },
                    {"text": prompt_text}
                ]
            }
        ]
    }

    resp = requests.post(GEMINI_REST_URL, headers=headers, json=body, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text}")
    
    # Parse response
    j = resp.json()
    
    # Extract token usage metadata
    input_tokens = 0
    output_tokens = 0
    
    # Gemini API returns usage metadata in usageMetadata field
    if "usageMetadata" in j:
        usage = j["usageMetadata"]
        input_tokens = usage.get("promptTokenCount", 0)
        output_tokens = usage.get("candidatesTokenCount", 0)
    
    # Extract text from response
    candidate_text = None
    if isinstance(j, dict):
        # Try to extract from candidates array (standard Gemini response format)
        if "candidates" in j and isinstance(j["candidates"], list) and len(j["candidates"]) > 0:
            candidate = j["candidates"][0]
            if "content" in candidate:
                content = candidate["content"]
                if "parts" in content and isinstance(content["parts"], list):
                    for part in content["parts"]:
                        if "text" in part:
                            candidate_text = part["text"]
                            break
        
        # Fallback to other fields
        if not candidate_text and "output" in j and isinstance(j["output"], str):
            candidate_text = j["output"]
        if not candidate_text and "text" in j and isinstance(j["text"], str):
            candidate_text = j["text"]
        
        # Recursive search for text as last resort
        if not candidate_text:
            def find_first_string(obj):
                if isinstance(obj, str):
                    return obj
                if isinstance(obj, dict):
                    for v in obj.values():
                        r = find_first_string(v)
                        if r:
                            return r
                if isinstance(obj, list):
                    for it in obj:
                        r = find_first_string(it)
                        if r:
                            return r
                return None
            candidate_text = find_first_string(j)
    
    if candidate_text is None:
        # fallback: return raw json string
        candidate_text = json.dumps(j)
    
    return candidate_text, input_tokens, output_tokens


def image_to_base64_str(path: str) -> str:
    """Reads an image file and returns a base64-encoded string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_first_json(s: str):
    """
    Extract the first valid JSON array from a string.
    Handles cases where the model wraps JSON in markdown code blocks.
    """
    import re
    
    # Remove markdown code blocks if present
    s = re.sub(r'^```(?:json)?\s*', '', s, flags=re.MULTILINE)
    s = re.sub(r'```\s*$', '', s, flags=re.MULTILINE)
    s = s.strip()
    
    # Try to parse as-is
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return parsed
        # If it's a dict with a single key that contains a list, unwrap it
        if isinstance(parsed, dict) and len(parsed) == 1:
            for v in parsed.values():
                if isinstance(v, list):
                    return v
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON array in the string
    # Look for [ ... ] pattern
    match = re.search(r'\[.*\]', s, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    raise ValueError("Could not extract valid JSON array from response")


def canonicalize_entry(parsed: dict) -> dict:
    """
    Convert parsed chunk dict into canonical form with proper types and validation.
    """
    text = parsed.get("text")
    page_number = parsed.get("page_number")
    metadata = parsed.get("metadata", {})

    # ensure metadata exists
    if metadata is None:
        metadata = {}

    # ensure lists or None
    def norm_list(v):
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # try to split comma-separated, else return single item list
            if "," in v:
                return [x.strip() for x in v.split(",") if x.strip()]
            return [v]
        return None

    topics = norm_list(metadata.get("topics"))
    subtopics = norm_list(metadata.get("subtopics"))
    prerequisites = norm_list(metadata.get("prerequisites"))

    chunk_type = metadata.get("chunk_type")
    if isinstance(chunk_type, str):
        ct = chunk_type.strip().lower()
        if ct not in ALLOWED_CHUNK_TYPES:
            ct = None
    else:
        ct = None

    difficulty = metadata.get("difficulty_level")
    if isinstance(difficulty, str):
        dl = difficulty.strip().lower()
        if dl not in ALLOWED_DIFFICULTY:
            dl = None
    else:
        dl = None

    source_url = metadata.get("source_url")
    source_type = metadata.get("source_type")

    out = {
        "text": text if text is not None else None,
        "page_number": int(page_number) if (page_number is not None) else None,
        "metadata": {
            "source_url": source_url if source_url is not None else None,
            "source_type": source_type if source_type is not None else None,
            "topics": topics,
            "subtopics": subtopics,
            "chunk_type": ct,
            "difficulty_level": dl,
            "prerequisites": prerequisites,
        },
    }
    return out


def process_folder(images_folder: str, out_json_path: str):
    """
    Process all images in `images_folder`. For each image:
      - encode image to base64
      - build a chunking prompt with build_prompt_for_chunks(...)
      - call Gemini via call_gemini_rest(...)
      - track token usage per image
      - save raw output to RAW_OUTPUT_DIR/<filename>.raw.txt
      - extract a JSON array of chunk objects via extract_first_json(...)
      - canonicalize each chunk with canonicalize_entry(...)
      - ensure page_number/chunk_index/metadata.source_url/source_type are set
      - optional dspy validation (best-effort)
      - append canonicalized chunks to results
    Finally writes the combined list of chunk objects to out_json_path.
    """
    import os, time, json

    os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
    results = []

    # Collect image files (sorted to maintain page order)
    files = sorted(
        [
            f
            for f in os.listdir(images_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".tiff", ".tif"))
        ]
    )

    if not files:
        print(f"No images found in '{images_folder}'.")
        return

    for idx, fname in enumerate(files, start=1):
        path = os.path.join(images_folder, fname)
        print(f"[{idx}/{len(files)}] Processing {path} ...")

        # Determine mime type from extension
        ext = fname.lower().rsplit(".", 1)[-1]
        mime = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "webp": "image/webp",
            "tiff": "image/tiff",
            "tif": "image/tiff",
        }.get(ext, "image/png")

        # Encode image
        try:
            img_b64 = image_to_base64_str(path)
        except Exception as e:
            print(f"  ERROR: Could not read/encode image {path}: {e}")
            continue

        # Build prompt and call Gemini
        prompt = build_prompt_for_chunks(fname, idx)
        try:
            raw_out, input_tokens, output_tokens = call_gemini_rest(img_b64, mime, prompt)
            print(f"  Tokens used: {input_tokens + output_tokens:,} (input: {input_tokens:,}, output: {output_tokens:,})")
        except Exception as e:
            print(f"  ERROR: Gemini API failed for {fname}: {e}")
            # Save error info for debugging
            err_path = os.path.join(RAW_OUTPUT_DIR, f"{fname}.error.txt")
            with open(err_path, "w", encoding="utf-8") as ef:
                ef.write(str(e))
            # Record zero tokens for failed request
            token_tracker.add_usage(fname, 0, 0, 0)
            continue

        # Save raw output for debugging
        raw_path = os.path.join(RAW_OUTPUT_DIR, f"{fname}.raw.txt")
        try:
            with open(raw_path, "w", encoding="utf-8") as rf:
                rf.write(raw_out)
        except Exception as e:
            print(f"  WARN: Could not save raw output for {fname}: {e}")

        # Attempt to extract JSON array of chunks
        try:
            parsed_chunks = extract_first_json(raw_out)  # expected: list of dicts
        except Exception as e:
            print(f"  WARN: Could not extract JSON array for {fname}: {e}")
            print(f"  Saved raw to {raw_path}; skipping entry.")
            # Record tokens even though parsing failed
            token_tracker.add_usage(fname, input_tokens, output_tokens, 0)
            continue

        chunk_count = 0
        # Canonicalize each chunk and append to results
        for chunk_idx, parsed in enumerate(parsed_chunks, start=1):
            # Defensive normalization
            if parsed is None or not isinstance(parsed, dict):
                print(f"  WARN: Skipping non-object chunk {chunk_idx} in {fname}")
                continue

            # Ensure page_number, chunk_index
            if parsed.get("page_number") is None:
                parsed["page_number"] = idx
            if parsed.get("chunk_index") is None:
                parsed["chunk_index"] = chunk_idx

            # Ensure metadata object and source fields
            if parsed.get("metadata") is None or not isinstance(parsed.get("metadata"), dict):
                parsed["metadata"] = {}
            if parsed["metadata"].get("source_url") is None:
                parsed["metadata"]["source_url"] = fname
            if parsed["metadata"].get("source_type") is None:
                parsed["metadata"]["source_type"] = "image"

            # Canonicalize to consistent shape (uses your canonicalize_entry implementation)
            try:
                entry = canonicalize_entry(parsed)
            except Exception as e:
                print(f"  WARN: canonicalization failed for chunk {chunk_idx} of {fname}: {e}")
                # Save problematic parsed chunk for debugging
                dbg_path = os.path.join(RAW_OUTPUT_DIR, f"{fname}.chunk{chunk_idx}.bad.json")
                try:
                    with open(dbg_path, "w", encoding="utf-8") as bf:
                        json.dump(parsed, bf, indent=2, ensure_ascii=False)
                    print(f"  Saved problematic chunk to {dbg_path}")
                except Exception:
                    pass
                continue

            # Attach chunk_index at top-level if not preserved by canonicalize_entry
            if parsed.get("chunk_index") is not None:
                try:
                    entry["chunk_index"] = int(parsed["chunk_index"])
                except Exception:
                    entry["chunk_index"] = chunk_idx
            else:
                entry["chunk_index"] = chunk_idx

            # dspy validation (best-effort)
            if DSPY_AVAILABLE:
                try:
                    # PageExtract.validate may be the validation call depending on your dspy version
                    PageExtract.validate(entry)
                except Exception as e:
                    print(f"  dspy validation warning for {fname} chunk {chunk_idx}: {e}")

            results.append(entry)
            chunk_count += 1

        # Record token usage for this image
        token_tracker.add_usage(fname, input_tokens, output_tokens, chunk_count)
        print(f"  Extracted {chunk_count} chunks from {fname}")

        # small throttle to avoid bursts
        time.sleep(REQUEST_SLEEP)

    # Write combined output
    try:
        with open(out_json_path, "w", encoding="utf-8") as outf:
            json.dump(results, outf, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(results)} entries to {out_json_path}.")
    except Exception as e:
        print(f"ERROR: Could not write combined output to {out_json_path}: {e}")
    
    # Write token usage statistics
    try:
        summary = token_tracker.get_summary()
        with open(STATS_OUTPUT_PATH, "w", encoding="utf-8") as sf:
            json.dump(summary, sf, indent=2, ensure_ascii=False)
        print(f"Saved token usage statistics to {STATS_OUTPUT_PATH}")
    except Exception as e:
        print(f"ERROR: Could not write token statistics to {STATS_OUTPUT_PATH}: {e}")
    
    # Print summary to console
    token_tracker.print_summary()

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    process_folder(IMAGES_FOLDER, OUTPUT_JSON_PATH)