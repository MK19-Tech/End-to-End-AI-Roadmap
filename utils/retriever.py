import os
import chromadb
from chromadb.utils import embedding_functions

# MATCH the logic in vector_store.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

def get_relevant_chunks(query, n_results=3):
    if not os.path.exists(DB_DIR):
        raise Exception(f"Database folder NOT FOUND at {DB_DIR}. Please run main.py first.")

    client = chromadb.PersistentClient(path=DB_DIR)
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    try:
        collection = client.get_collection(name="my_documents", embedding_function=model)
        results = collection.query(query_texts=[query], n_results=n_results)
        return results["documents"][0] 
    except Exception as e:
        existing = client.list_collections()
        raise Exception(f"Collection 'my_documents' not found. Available: {existing}")
