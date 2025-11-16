
from agents.retrieval.backend.rag_system import RAGSystem, initialize_rag_system
from agents.retrieval.backend import RETRIEVAL_BACKEND_PATH

def initialize_database(db_path: str = f"{RETRIEVAL_BACKEND_PATH}/vector_db", chunks_dir: str = None):
    """Initialize the RAG database with content."""
    print("\n" + "=" * 70)
    print("  RAG DATABASE INITIALIZATION")
    print("=" * 70)

    # Initialize RAG system
    print("\n🔧 Initializing RAG System...")
    try:
        rag_system = RAGSystem(db_path=db_path)
        print("   ✓ RAG System initialized")
    except Exception as e:
        print(f"   ✗ Error initializing RAG System: {e}")
        return False
    
    # Initialize with chunks
    print(f"\n📥 Loading chunks from {chunks_dir}...")
    try:
        initialize_rag_system(rag_system, chunks_dir=chunks_dir)
        print("   ✓ Chunks loaded successfully")
    except Exception as e:
        print(f"   ✗ Error loading chunks: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Verify
    chunk_count = rag_system.collection.count()
    print(f"\n✓ Database initialized with {chunk_count} chunks")
    print("=" * 70 + "\n")
    
    return True
