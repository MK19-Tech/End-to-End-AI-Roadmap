import os
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

def get_relevant_chunks(query, n_results=6): # Increased results for better coverage
    if not os.path.exists(DB_DIR):
        raise Exception(f"Database NOT FOUND at {DB_DIR}. Run main.py first.")

    client = chromadb.PersistentClient(path=DB_DIR)
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    try:
        collection = client.get_collection(name="my_documents", embedding_function=model)
        # We fetch more results so the Agent has a wider "vision"
        results = collection.query(query_texts=[query], n_results=n_results)
        return results["documents"][0]
    except Exception as e:
        return []
