import os
import chromadb
from chromadb.utils import embedding_functions

# Get the directory where the main project sits (2 levels up from this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

def add_to_vector_db(chunks, source_name):
    client = chromadb.PersistentClient(path=DB_DIR)
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.get_or_create_collection(name="my_documents", embedding_function=model)
    
    ids = [f"{source_name}_{i}" for i in range(len(chunks))]
    
    if chunks:
        collection.add(documents=chunks, ids=ids)
        print(f"DEBUG: Saved {len(chunks)} items. Total in DB: {collection.count()} at {DB_DIR}")
        return len(ids)
    return 0
