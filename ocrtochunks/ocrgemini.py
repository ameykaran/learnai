"""
images_to_structured_json_gemini_rest.py

- Sends images (from folder) to Gemini 2.5 Flash via REST (API key auth).
- Asks Gemini to OCR and produce structured JSON per the requested schema.
- Enforces LaTeX rendering for math.
- Produces one combined JSON with page_number field in each entry.
- Stores raw model outputs for debugging on parse errors.

Notes:
- Inline image data has a ~20MB total request limit (image + prompt). For larger images, use the Files API (not implemented here).
- Endpoint used (REST): https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent
- Auth header: x-goog-api-key: <API_KEY>
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
IMAGES_FOLDER = "output_images_full"   # folder with page_1.png etc
OUTPUT_JSON_PATH = "completeTB/combined_structured.json"
RAW_OUTPUT_DIR = "completeTB/raw_model_outputs"
REQUEST_SLEEP = 0.15  # small throttle (seconds) between requests to avoid burst limits

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


# -------------------------
# Build strict prompt
# -------------------------
# def build_prompt(filename: str, page_number: int) -> str:
#     """
#     Strict prompt instructing Gemini to:
#     - Extract text (OCR)
#     - Render all math as LaTeX (use $...$ for inline, $$...$$ for display)
#     - Fill metadata, use null for missing fields
#     - Return EXACTLY one JSON object (no commentary)
#     """
#     prompt = rf"""
# You are an OCR and semantic annotator.

# I will give you an image of a textbook page (filename: "{filename}", page_number: {page_number}).
# Do the following and return EXACTLY one JSON object (no explanation, no surrounding backticks):

# 1) Extract the visible textual content from the page. Render all mathematical expressions and formulas as LaTeX:
#    - Use inline math $...$ for inline expressions and $$...$$ for display equations.
#    - If an equation spans multiple lines, use $$ ... $$ and include line breaks within the LaTeX where appropriate.
#    - Keep text faithful to what is present on the page (do not invent extra text).

# 2) Fill the metadata with these fields:
#    - source_url: set to the filename string (e.g., "{filename}")
#    - source_type: "image" (string)
#    - topics: list of high-level topics (strings) or null if unknown
#    - subtopics: list of subtopics (strings) or null if unknown
#    - chunk_type: one of ["definition","example","explanation","proof","visualization","practice_problem","worked_solution","analogy","misconception"] or null
#    - difficulty_level: one of ["basic","intermediate","advanced"] or null
#    - prerequisites: list of short prerequisite phrases (strings) or null

# 3) Include page_number as an integer field in the top-level object.

# 4) If any field cannot be determined from the page, set that field to null (not an empty string).
# 5) The JSON must use null for missing values, not "None" or other tokens.

# Return JSON with this exact top-level shape:

# {{
#   "text": <string or null>,
#   "page_number": <int>,
#   "metadata": {{
#     "source_url": <string>,
#     "source_type": <string>,
#     "topics": <list of strings or null>,
#     "subtopics": <list of strings or null>,
#     "chunk_type": <string or null>,
#     "difficulty_level": <string or null>,
#     "prerequisites": <list of strings or null>
#   }}
# }}

# Important: Use LaTeX for math. Example: P(A \mid B) = \frac{{P(A \cap B)}}{{P(B)}} rendered as $P(A \mid B) = \frac{{P(A \cap B)}}{{P(B)}}$.

# Do not emit any text besides the JSON object.
# """
#     return prompt.strip()

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



# -------------------------
# Call Gemini REST
# -------------------------
def call_gemini_rest(image_b64: str, mime_type: str, prompt_text: str) -> str:
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
    # Response JSON structure contains generated text. We'll try to extract text in robust ways.
    j = resp.json()
    # look through likely keys for text
    # Some responses place text under 'candidates' or 'output' or 'text'; handle common patterns
    candidate_text = None
    # top-level 'candidates' style
    if isinstance(j, dict):
        # try common fields
        if "output" in j and isinstance(j["output"], str):
            candidate_text = j["output"]
        if not candidate_text and "text" in j and isinstance(j["text"], str):
            candidate_text = j["text"]
        # Vertex/GenAI sometimes uses "candidates" or "results"
        if not candidate_text:
            # recursively search for first string value
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
        return json.dumps(j)
    return candidate_text


def image_to_base64_str(path: str) -> str:
    """Reads an image file and returns a base64-encoded string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# -------------------------
# Extract first JSON object from model output text
# -------------------------
# def extract_first_json(s: str) -> Dict[str, Any]:
#     """Heuristic: find first {...} and parse it. """
#     start = s.find("{")
#     end = s.rfind("}")
#     if start == -1 or end == -1 or end <= start:
#         raise ValueError("No JSON object detected in model output.")
#     jtext = s[start:end+1]
#     return json.loads(jtext)

def extract_first_json(s: str):
    """
    Extract the first JSON object or JSON array found in model output.
    Returns a Python list of chunk dicts.
    """
    import json, re

    # Try to find the first JSON array [...] or object {...}
    # Prefer array if present.
    array_match = re.search(r"\[\s*\{", s, flags=re.DOTALL)
    if array_match:
        # find first top-level matching bracket range for array
        start = s.find("[", array_match.start())
        # naive but practical: find last closing ']' after start
        end = s.rfind("]")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON array detected in model output.")
        json_text = s[start:end+1]
    else:
        # fallback to first object
        start = s.find("{")
        end = s.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object detected in model output.")
        json_text = s[start:end+1]
        # wrap single object into list for consistent downstream handling
        json_text = f"[{json_text}]"

    parsed = json.loads(json_text)
    if not isinstance(parsed, list):
        raise ValueError("Parsed JSON is not a list of objects.")
    return parsed

# -------------------------
# Canonicalize parsed object to required shape
# -------------------------
def canonicalize_entry(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure fields exist and use None for missing values; also lowercase chunk_type/difficulty when present.
    """
    # top-level keys
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


# -------------------------
# Process folder
# -------------------------
# def process_folder(images_folder: str, out_json_path: str):
#     os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
#     results = []
#     files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".tiff"))])
#     for idx, fname in enumerate(files, start=1):
#         path = os.path.join(images_folder, fname)
#         print(f"[{idx}/{len(files)}] Processing {path} ...")
#         # determine mime type by extension
#         ext = fname.lower().split(".")[-1]
#         mime = {
#             "png": "image/png",
#             "jpg": "image/jpeg",
#             "jpeg": "image/jpeg",
#             "webp": "image/webp",
#             "tiff": "image/tiff",
#             "tif": "image/tiff"
#         }.get(ext, "image/png")

#         img_b64 = image_to_base64_str(path)
#         prompt = build_prompt(fname, idx)  # page_number uses index order (1-based)
#         try:
#             raw_out = call_gemini_rest(img_b64, mime, prompt)
#         except Exception as e:
#             print(f"  ERROR: Gemini API failed for {fname}: {e}")
#             # Save error info
#             with open(os.path.join(RAW_OUTPUT_DIR, f"{fname}.error.txt"), "w", encoding="utf-8") as ef:
#                 ef.write(str(e))
#             continue

#         # Save raw output for debugging
#         raw_path = os.path.join(RAW_OUTPUT_DIR, f"{fname}.raw.txt")
#         with open(raw_path, "w", encoding="utf-8") as rf:
#             rf.write(raw_out)

#         # Attempt to extract JSON
#         try:
#             parsed = extract_first_json(raw_out)
#         except Exception as e:
#             print(f"  WARN: Could not extract JSON for {fname}: {e}")
#             print(f"  Saved raw to {raw_path}; skipping entry.")
#             continue

#         # Canonicalize and append
#         entry = canonicalize_entry(parsed)
#         # Ensure that page_number is the index we expect if not present
#         if entry.get("page_number") is None:
#             entry["page_number"] = idx
#             # Also set metadata.source_url if missing
#             if entry["metadata"].get("source_url") is None:
#                 entry["metadata"]["source_url"] = fname
#             if entry["metadata"].get("source_type") is None:
#                 entry["metadata"]["source_type"] = "image"

#         # Optional: dspy validation (best-effort)
#         if DSPY_AVAILABLE:
#             try:
#                 PageExtract.validate(entry)  # may raise
#             except Exception as e:
#                 print(f"  dspy validation warning for {fname}: {e}")

#         results.append(entry)
#         # small sleep to not burst
#         time.sleep(REQUEST_SLEEP)

#     # write combined output
#     with open(out_json_path, "w", encoding="utf-8") as outf:
#         json.dump(results, outf, indent=2, ensure_ascii=False)

#     print(f"Saved {len(results)} entries to {out_json_path}. Raw outputs in {RAW_OUTPUT_DIR}/")

def process_folder(images_folder: str, out_json_path: str):
    """
    Process all images in `images_folder`. For each image:
      - encode image to base64
      - build a chunking prompt with build_prompt_for_chunks(...)
      - call Gemini via call_gemini_rest(...)
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
            raw_out = call_gemini_rest(img_b64, mime, prompt)
        except Exception as e:
            print(f"  ERROR: Gemini API failed for {fname}: {e}")
            # Save error info for debugging
            err_path = os.path.join(RAW_OUTPUT_DIR, f"{fname}.error.txt")
            with open(err_path, "w", encoding="utf-8") as ef:
                ef.write(str(e))
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
            continue

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

        # small throttle to avoid bursts
        time.sleep(REQUEST_SLEEP)

    # Write combined output
    try:
        with open(out_json_path, "w", encoding="utf-8") as outf:
            json.dump(results, outf, indent=2, ensure_ascii=False)
        print(f"Saved {len(results)} entries to {out_json_path}. Raw outputs in {RAW_OUTPUT_DIR}/")
    except Exception as e:
        print(f"ERROR: Could not write combined output to {out_json_path}: {e}")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    process_folder(IMAGES_FOLDER, OUTPUT_JSON_PATH)
