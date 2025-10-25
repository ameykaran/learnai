"""
Hybrid RAG System with Vector and Metadata Filtering

This module implements a Retrieval-Augmented Generation (RAG) system that combines:
- Vector-based semantic search using sentence embeddings
- Metadata filtering for both scalar and list-based attributes
- Persistent storage using ChromaDB

The system handles ChromaDB's limitation with list metadata by serializing lists
as tagged strings within the document content, enabling efficient filtering.
"""

import uuid
import json
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import chromadb

from schema import Chunk, Metadata


class RAGSystem:
    """
    A hybrid Retrieval-Augmented Generation system combining vector search with metadata filtering.
    
    This system stores educational content chunks with rich metadata and enables efficient
    retrieval using both semantic similarity and structured filters.
    
    Attributes:
        LIST_FIELDS (set): Metadata fields containing lists (stored in document text)
        SCALAR_FIELDS (set): Metadata fields containing scalar values (stored in ChromaDB metadata)
        embedding_model: SentenceTransformer model for creating text embeddings
        client: ChromaDB persistent client
        collection: ChromaDB collection storing the chunks
    """
    
    # Define which metadata fields are lists vs scalars
    LIST_FIELDS = {"topics", "subtopics", "prerequisites"}
    SCALAR_FIELDS = {"source_url", "source_type", "chunk_type", "difficulty_level"}
    
    def __init__(self, db_path: str = "./chroma_db", model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the RAG system with embedding model and vector database.
        
        Args:
            db_path: Path to store the ChromaDB persistent database
            model_name: Name of the SentenceTransformer model to use for embeddings
        
        Example:
            >>> rag = RAGSystem(db_path="./my_db")
            Initializing RAG System...
            Embedding model loaded.
            ChromaDB collection 'educational_chunks' loaded/created from ./my_db.
            0 chunks currently in the database.
        """
        print("Initializing RAG System...")
        
        # Initialize the embedding model
        self.embedding_model = SentenceTransformer(model_name)
        print("Embedding model loaded.")

        # Initialize the ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create a collection with cosine similarity
        self.collection = self.client.get_or_create_collection(
            name="educational_chunks",
            metadata={"hnsw:space": "cosine"}
        )
        print(f"ChromaDB collection 'educational_chunks' loaded/created from {db_path}.")
        print(f"{self.collection.count()} chunks currently in the database.")

    def _embed(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        return self.embedding_model.encode(text).tolist()

    def _serialize_list(self, data: List[str], tag: str) -> str:
        """
        Serialize a list of strings into a tagged string for document filtering.
        
        This method converts list metadata into a searchable format that can be
        stored in the document text and filtered using ChromaDB's $contains operator.
        
        Args:
            data: List of strings to serialize
            tag: Tag name to identify the list type (e.g., "TOPICS", "SUBTOPICS")
            
        Returns:
            Tagged string representation of the list, or empty string if list is empty
            
        Example:
            >>> self._serialize_list(["Python", "SQL"], "TOPICS")
            ' <META_TOPICS:,Python,SQL,> '
        """
        if not data:
            return ""
        return f" <META_{tag.upper()}:,{','.join(data)},> "

    def _deserialize_list(self, document: str, tag: str) -> List[str]:
        """
        Extract a serialized list from a document string.
        
        Args:
            document: Document text containing serialized lists
            tag: Tag name to identify the list type
            
        Returns:
            List of extracted strings, or empty list if tag not found
        """
        start_tag = f" <META_{tag}:,"
        end_tag = ",> "
        
        if start_tag in document:
            start_idx = document.index(start_tag) + len(start_tag)
            end_idx = document.index(end_tag, start_idx)
            list_str = document[start_idx:end_idx]
            return [item for item in list_str.split(',') if item]
        return []

    def _remove_metadata_tags(self, text: str) -> str:
        """
        Remove all serialized metadata tags from document text.
        
        Args:
            text: Document text with metadata tags
            
        Returns:
            Cleaned text without metadata tags
        """
        doc_text = text
        for tag in ["TOPICS", "SUBTOPICS", "PREREQS"]:
            start_tag = f" <META_{tag}:,"
            end_tag = ",> "
            while start_tag in doc_text:
                start_idx = doc_text.index(start_tag)
                end_idx = doc_text.index(end_tag, start_idx) + len(end_tag)
                doc_text = doc_text[:start_idx] + doc_text[end_idx:]
        return doc_text.strip()

    def add_chunks(self, chunks: List[Chunk]) -> None:
        """
        Add a batch of chunks to the vector store.
        
        This method:
        1. Serializes list metadata into document text for filtering
        2. Creates embeddings from the original text
        3. Stores scalar metadata separately
        4. Batch-inserts all data into ChromaDB
        
        Args:
            chunks: List of Chunk objects to add
            
        Example:
            >>> chunks = [Chunk(...), Chunk(...)]
            >>> rag.add_chunks(chunks)
            Adding 2 chunks to the database...
            Successfully added 2 chunks.
        """
        if not chunks:
            print("No chunks to add.")
            return
            
        print(f"\nAdding {len(chunks)} chunks to the database...")
        
        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for chunk in chunks:
            # 1. Append serialized list metadata to document text
            doc_text = chunk.text
            doc_text += self._serialize_list(chunk.metadata.topics, "TOPICS")
            doc_text += self._serialize_list(chunk.metadata.subtopics, "SUBTOPICS")
            doc_text += self._serialize_list(chunk.metadata.prerequisites, "PREREQS")
            documents.append(doc_text)
            
            # 2. Create embedding from original text only
            embeddings.append(self._embed(chunk.text))
            
            # 3. Store scalar metadata in ChromaDB metadata field
            meta_dict = {
                "source_url": chunk.metadata.source_url,
                "source_type": chunk.metadata.source_type,
                "chunk_type": chunk.metadata.chunk_type,
                "difficulty_level": chunk.metadata.difficulty_level,
            }
            metadatas.append(meta_dict)
            
            # 4. Use chunk ID
            ids.append(chunk.id)
        
        # Batch-add all data to ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {len(chunks)} chunks.")

    def _build_filters(self, filters: Dict[str, Any]) -> Tuple[Optional[Dict], Optional[Dict]]:
        """
        Split filters into ChromaDB-compatible where and where_document filters.
        
        This method automatically routes filters to the appropriate ChromaDB filter type:
        - Scalar fields (source_url, chunk_type, etc.) → where filter
        - List fields (topics, subtopics, prerequisites) → where_document filter
        
        Args:
            filters: Dictionary of filter conditions
            
        Returns:
            Tuple of (where_filter, where_document_filter), either may be None
            
        Example:
            >>> filters = {"difficulty_level": "basic", "topics": "Python"}
            >>> where, where_doc = self._build_filters(filters)
            >>> where
            {'difficulty_level': {'$eq': 'basic'}}
            >>> where_doc
            {'$contains': '<META_TOPICS:,Python,'}
        """
        where_conditions = []
        where_document_conditions = []
        
        for key, value in filters.items():
            if key in self.SCALAR_FIELDS:
                # Scalar metadata: use $eq operator
                where_conditions.append({key: {"$eq": value}})
                
            elif key in self.LIST_FIELDS:
                # List metadata: search in serialized document tags
                tag_mapping = {
                    "topics": "TOPICS",
                    "subtopics": "SUBTOPICS",
                    "prerequisites": "PREREQS"
                }
                tag = tag_mapping[key]
                
                # Handle both single values and lists
                values = value if isinstance(value, list) else [value]
                
                # Create $contains condition for each value
                for val in values:
                    where_document_conditions.append(
                        {"$contains": f"<META_{tag}:,{val},"}
                    )
            else:
                print(f"Warning: Unknown filter key '{key}' ignored.")
        
        # Build where_filter with ChromaDB $and operator for multiple conditions
        where_filter = None
        if where_conditions:
            where_filter = where_conditions[0] if len(where_conditions) == 1 else {"$and": where_conditions}
        
        # Build where_document_filter
        where_document_filter = None
        if where_document_conditions:
            where_document_filter = (
                where_document_conditions[0] if len(where_document_conditions) == 1 
                else {"$and": where_document_conditions}
            )
        
        return (where_filter, where_document_filter)

    def query(
        self,
        query_text: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        verbose: bool = True
    ) -> List[Chunk]:
        """
        Perform hybrid search combining vector similarity with metadata filtering.
        
        This method:
        1. Converts filters to ChromaDB-compatible format
        2. Creates query embedding
        3. Performs filtered vector search
        4. Reconstructs Chunk objects with complete metadata
        
        Args:
            query_text: Natural language query text
            k: Number of results to return (default: 5)
            filters: Optional metadata filters as key-value pairs
            verbose: Whether to print search information (default: True)
            
        Returns:
            List of Chunk objects matching the query, ordered by similarity
            
        Example:
            >>> results = rag.query(
            ...     query_text="explain probability distributions",
            ...     k=3,
            ...     filters={"difficulty_level": "intermediate", "topics": "Statistics"}
            ... )
            Query: 'explain probability distributions'
            Input Filters: {'difficulty_level': 'intermediate', 'topics': 'Statistics'}
            Found 3 results.
        """
        if verbose:
            print(f"Query: '{query_text}'")
        
        # Build ChromaDB filters from input
        where_filter, where_document_filter = None, None
        if filters:
            if verbose:
                print(f"Input Filters: {filters}")
            where_filter, where_document_filter = self._build_filters(filters)

        # Create query embedding
        query_embedding = self._embed(query_text)
        
        # Execute ChromaDB query
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where_filter,
            where_document=where_document_filter
        )
        
        # Reconstruct Chunk objects from results
        cleaned_results = []
        for i in range(len(results['ids'][0])):
            original_doc = results['documents'][0][i]
            
            # Remove metadata tags from document text
            clean_text = self._remove_metadata_tags(original_doc)

            # Reconstruct metadata dictionary
            metadata_dict = results['metadatas'][0][i].copy()
            
            # Extract list fields from serialized tags
            metadata_dict['topics'] = self._deserialize_list(original_doc, "TOPICS")
            metadata_dict['subtopics'] = self._deserialize_list(original_doc, "SUBTOPICS")
            metadata_dict['prerequisites'] = self._deserialize_list(original_doc, "PREREQS")

            # Create Chunk object
            chunk = Chunk(
                id=results['ids'][0][i],
                text=clean_text,
                metadata=Metadata(**metadata_dict)
            )
            cleaned_results.append(chunk)

        if verbose:
            print(f"Found {len(cleaned_results)} results.")
        return cleaned_results

    def clear_collection(self) -> None:
        """
        Delete all chunks from the collection.
        
        Warning: This operation cannot be undone.
        
        Example:
            >>> rag.clear_collection()
            Cleared 150 chunks from the database.
        """
        count = self.collection.count()
        if count > 0:
            self.collection.delete(ids=self.collection.get()['ids'])
            print(f"Cleared {count} chunks from the database.")
        else:
            print("Collection is already empty.")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current collection.
        
        Returns:
            Dictionary containing collection statistics
            
        Example:
            >>> stats = rag.get_stats()
            >>> print(stats)
            {'total_chunks': 150, 'collection_name': 'educational_chunks'}
        """
        return {
            'total_chunks': self.collection.count(),
            'collection_name': self.collection.name
        }


# --- Helper Functions ---

def load_chunks_from_json(filepath: str) -> List[Chunk]:
    """
    Load chunks from a JSON file.
    
    Args:
        filepath: Path to JSON file containing chunk data
        
    Returns:
        List of Chunk objects
        
    Expected JSON format:
        [
            {
                "text": "Content text...",
                "metadata": {
                    "source_url": "...",
                    "source_type": "...",
                    "chunk_type": "...",
                    "difficulty_level": "...",
                    "topics": [...],
                    "subtopics": [...],
                    "prerequisites": [...]
                }
            },
            ...
        ]
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []
    for item in data:
        chunk = Chunk(
            id=uuid.uuid4().hex,
            text=item['text'],
            metadata=Metadata(
                source_url=item['metadata']['source_url'],
                source_type=item['metadata']['source_type'],
                chunk_type=item['metadata']['chunk_type'],
                difficulty_level=item['metadata']['difficulty_level'],
                topics=item['metadata'].get('topics', []),
                subtopics=item['metadata'].get('subtopics', []),
                prerequisites=item['metadata'].get('prerequisites', [])
            )
        )
        chunks.append(chunk)
    return chunks


def initialize_rag_system(rag_system: RAGSystem, chunks_file: str = "extracted_chunks.json") -> None:
    """
    Initialize RAG system with chunks from a JSON file.
    
    This function clears the existing collection and loads fresh data.
    
    Args:
        rag_system: RAGSystem instance to initialize
        chunks_file: Path to JSON file containing chunks
    """
    print("\n" + "="*60)
    print("INITIALIZING RAG SYSTEM")
    print("="*60)
    
    # Clear existing data
    rag_system.clear_collection()
    
    # Load and add chunks
    chunks = load_chunks_from_json(chunks_file)
    rag_system.add_chunks(chunks)
    
    print("Initialization complete.")


# --- Main Demo ---

if __name__ == "__main__":
    # Initialize the system
    rag_system = RAGSystem(db_path="./prob_db")
    
    # Load data (comment out if collection is already populated)
    initialize_rag_system(rag_system)

    print(f"\nCurrent stats: {rag_system.get_stats()}")

    # --- TEST 1: Pure Vector Search ---
    print("\n" + "="*60)
    print("TEST 1: Pure Vector Search (no filters)")
    print("="*60)
    results = rag_system.query(
        query_text="probability distributions and random variables",
        k=3
    )
    for i, chunk in enumerate(results, 1):
        print(f"\n[Result {i}]")
        print(f"Text: {chunk.text[:200]}...")
        print(f"Type: {chunk.metadata.chunk_type} | Level: {chunk.metadata.difficulty_level}")
        print(f"Topics: {', '.join(chunk.metadata.topics)}")

    # --- TEST 2: Scalar Metadata Filter ---
    print("\n" + "="*60)
    print("TEST 2: Scalar Metadata Filter")
    print("="*60)
    results = rag_system.query(
        query_text="basic concepts",
        k=3,
        filters={
            "difficulty_level": "basic",
            "chunk_type": "definition"
        }
    )
    for i, chunk in enumerate(results, 1):
        print(f"\n[Result {i}]")
        print(f"Text: {chunk.text[:200]}...")
        print(f"Metadata: {chunk.metadata.chunk_type} | {chunk.metadata.difficulty_level}")

    # --- TEST 3: List-based Filter ---
    print("\n" + "="*60)
    print("TEST 3: List-based Filter (topics)")
    print("="*60)
    results = rag_system.query(
        query_text="statistical concepts",
        k=3,
        filters={
            "topics": "Statistics"
        }
    )
    for i, chunk in enumerate(results, 1):
        print(f"\n[Result {i}]")
        print(f"Text: {chunk.text[:200]}...")
        print(f"Topics: {', '.join(chunk.metadata.topics)}")

    # --- TEST 4: Combined Filters ---
    print("\n" + "="*60)
    print("TEST 4: Combined Filters (scalar + list)")
    print("="*60)
    results = rag_system.query(
        query_text="fundamental probability concepts",
        k=3,
        filters={
            "topics": "Probability",
            "difficulty_level": "basic",
            "chunk_type": "definition"
        }
    )
    for i, chunk in enumerate(results, 1):
        print(f"\n[Result {i}]")
        print(f"Text: {chunk.text[:200]}...")
        print(f"Topics: {', '.join(chunk.metadata.topics)}")
        print(f"Level: {chunk.metadata.difficulty_level} | Type: {chunk.metadata.chunk_type}")
