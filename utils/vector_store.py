import os
import chromadb
from chromadb.utils import embedding_functions

# Silences the warnings you saw earlier
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def add_to_vector_db(chunks, source_name, db_path="./chroma_db"):
    """STEP 6: Vector Storage with Verification"""
    
    # 1. Initialize the local database
    # This creates the 'chroma_db' folder if it doesn't exist
    client = chromadb.PersistentClient(path=db_path)
    
    # 2. Choose the embedding model (Meaning Maker)
    model = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # 3. Create or get the collection
    # 'get_or_create' is vital to prevent the "not found" error in search.py
    collection = client.get_or_create_collection(
        name="my_documents", 
        embedding_function=model
    )
    
    # 4. Prepare unique IDs and Metadata
    # We use the filename + index to ensure IDs are unique
    ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
    metadata = [{"source": source_name} for _ in range(len(chunks))]
    
    # 5. Add to database
    if chunks:
        collection.add(
            documents=chunks,
            metadatas=metadata,
            ids=ids
        )
        
        # --- VERIFICATION STEP ---
        # Let's double check it actually saved
        new_count = collection.count()
        print(f"--- Verification: DB now contains {new_count} total chunks ---")
        
        return len(ids)
    else:
        print(f"--- Warning: No chunks provided for {source_name} ---")
        return 0
