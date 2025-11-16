
from agents.retrieval.backend.rag_system import RAGSystem, initialize_rag_system
from agents.retrieval.backend import RETRIEVAL_BACKEND_PATH

def initialize_database(db_path: str = f"{RETRIEVAL_BACKEND_PATH}/vector_db", chunks_file: str = None):
    """Initialize the RAG database with content."""
    print("\n" + "=" * 70)
    print("  RAG DATABASE INITIALIZATION")
    print("=" * 70)
    
    # Determine chunks file
    if chunks_file is None:
        # Try to find a chunks file
        possible_files = [
            "rag/extracted_chunks.json",
            "rag/extracted_chunks-small.json",
            "rag/extracted_chunks-test.json",
        ]
        
        print("\n🔍 Looking for chunks file...")
        for possible_file in possible_files:
            if Path(possible_file).exists():
                chunks_file = possible_file
                print(f"   ✓ Found: {chunks_file}")
                break
        
        if chunks_file is None:
            print("   ✗ No chunks file found!")
            print("\n   Looked in:")
            for pf in possible_files:
                print(f"      - {pf}")
            print("\n   Please specify a chunks file with --file option")
            return False
    else:
        if not Path(chunks_file).exists():
            print(f"\n✗ Specified chunks file not found: {chunks_file}")
            return False
        print(f"\n✓ Using chunks file: {chunks_file}")
    
    # Initialize RAG system
    print("\n🔧 Initializing RAG System...")
    try:
        rag_system = RAGSystem(db_path=db_path)
        print("   ✓ RAG System initialized")
    except Exception as e:
        print(f"   ✗ Error initializing RAG System: {e}")
        return False
    
    # Initialize with chunks
    print(f"\n📥 Loading chunks from {chunks_file}...")
    try:
        initialize_rag_system(rag_system, chunks_file=chunks_file)
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
