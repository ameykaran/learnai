from keyword_extractor.keyword_extractor import KeywordExtractor
from rag.rag_system import RAGSystem
import dspy


from typing import List, Literal


class MetadataExtractor(dspy.Signature):
    query: str = dspy.InputField(
        desc="User query about a concept.")
    
    chunk_type: Literal["definition", "example", "explanation", "proof", "visualization", "practice_problem", "worked_solution", "analogy", "misconception"] = dspy.OutputField(
        desc="Type of chunk to extract.")
    difficulty_level: Literal["basic", "intermediate", "advanced"] = dspy.OutputField(
        desc="Difficulty level of the chunk."


class RAGChat:
    def __init__(self, rag_system: RAGSystem, keyword_extractor: KeywordExtractor):
        self.rag_system=rag_system
        self.keyword_extractor=keyword_extractor

        # Configure DSPy with Gemini LLM
        self.lm = dspy.LM(
            model="gemini/gemini-2.5-flash",
            api_key=gemini_api_key or "",  # Uses env variable if not provided
            max_tokens=chunk_size * 3,     # Allow extra tokens for structured output
            num_retries=MAX_RETRIES,
            temperature=temperature
        )
        dspy.configure(lm=lm)
        dspy.settings.configure(track_usage=True)


    def chat(self, user_input: str) -> str:
        keywords=self.keyword_extractor.extract_keywords(user_input)
        extractor = dspy.Predict(MetadataExtractor)
        filters={"topics": keywords, "difficulty_level": extractor.difficulty_level, "chunk_type": extractor.chunk_type}
        print("Applying filters:", filters)

        response=self.rag_system.query(user_input, filters=filters, k=3)

        return response


if __name__ == "__main__":
    # Example usage
    rag_system = RAGSystem(db_path="./rag/prob_db")

    extractor = KeywordExtractor(
        keywords_file="keyword_extractor/probability_keywords.csv",
        model_path="keyword_extractor/math_ner_model"
    )
    rag_chat = RAGChat(rag_system, keyword_extractor)

    user_query = "Explain the concept of derivatives in calculus."
    answer = rag_chat.chat(user_query)
    print("RAG Chat Response:", answer)
