import os
import chromadb
from chromadb.utils import embedding_functions

# Use the EXACT same absolute path logic
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def get_relevant_chunks(query, n_results=3):
    # Check if folder exists before even trying
    if not os.path.exists(DB_DIR):
        raise Exception(f"Database folder NOT FOUND at {DB_DIR}. Run main.py first.")

    client = chromadb.PersistentClient(path=DB_DIR)
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    try:
        # Don't use get_or_create here; we want to see if it actually exists
        collection = client.get_collection(name="my_documents", embedding_function=model)
        
        results = collection.query(query_texts=[query], n_results=n_results)
        return results["documents"][0] # Return the list of strings
    except Exception as e:
        # If it fails, list what collections actually DO exist to help debug
        existing = client.list_collections()
        raise Exception(f"Collection not found. Available collections: {existing}")
