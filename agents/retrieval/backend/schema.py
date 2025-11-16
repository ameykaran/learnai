from pydantic import BaseModel, Field
import uuid
from typing import List, Literal


class Metadata(BaseModel):
    source_url: str
    source_type: str
    topics: List[str]
    # subtopics: List[str]
    chunk_type: Literal["definition", "example", "explanation", "proof", "visualization",
                        "practice_problem", "worked_solution", "analogy", "misconception"]
    difficulty_level: Literal["basic", "intermediate", "advanced"]
    prerequisites: List[str]

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    metadata: Metadata
