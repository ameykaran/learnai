from keyword_extractor.keyword_extractor import KeywordExtractor
from rag.rag_system import RAGSystem, initialize_rag_system
import dspy
from typing import List, Literal
from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()

# Configuration constants
MAX_RETRIES = 3        # Number of retries for failed API calls

class MetadataExtractor(dspy.Signature):
    query: str = dspy.InputField(
        desc="User query about a concept.")
    
    chunk_type: Literal["definition", "example", "explanation", "proof", "visualization", "practice_problem", "worked_solution", "analogy", "misconception"] = dspy.OutputField(
        desc="Type of chunk to extract.")


class RAGChat:
    def __init__(self, rag_system: RAGSystem, keyword_extractor: KeywordExtractor):
        self.rag_system=rag_system
        self.keyword_extractor=keyword_extractor

        # Configure DSPy with Gemini LLM
        self.lm = dspy.LM(
            model="gemini/gemini-2.5-flash",
            max_tokens=5000 * 3,     # Allow extra tokens for structured output
            num_retries=MAX_RETRIES,
            temperature=0.2
        )
        dspy.configure(lm=self.lm)
        dspy.settings.configure(track_usage=True)


    def chat(self, user_input: str) -> str:
        keywords=self.keyword_extractor.extract_keywords(user_input)
        extractor = dspy.Predict(MetadataExtractor)
        extractor_output = extractor(query=user_input)
        filters={"topics": [kw.lower() for kw in keywords], 
                  "chunk_type": extractor_output.chunk_type}

        response=self.rag_system.query(user_input, filters=filters, k=3)

        return response


if __name__ == "__main__":
    # Example usage
    rag_system = RAGSystem(db_path="./rag/prob_db")
    # initialize_rag_system(rag_system, chunks_file="rag/extracted_chunks.json")

    keyword_extractor = KeywordExtractor(
        keywords_file="keyword_extractor/probability_keywords.csv",
        model_path="keyword_extractor/math_ner_model"
    )
    rag_chat = RAGChat(rag_system, keyword_extractor)

    while True:
        user_query = input("Enter your question (or 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        answer = rag_chat.chat(user_query)
        print("RAG Chat Response:", answer)
