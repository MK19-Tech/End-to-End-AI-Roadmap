import os
import chromadb
from chromadb.utils import embedding_functions

# Set the path to be absolute (e.g., C:/Users/.../my_project/chroma_db)
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def add_to_vector_db(chunks, source_name):
    # Initialize client with absolute path
    client = chromadb.PersistentClient(path=DB_DIR)
    
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Force get_or_create_collection
    collection = client.get_or_create_collection(name="my_documents", embedding_function=model)
    
    ids = [f"{source_name}_{i}" for i in range(len(chunks))]
    
    if chunks:
        collection.add(documents=chunks, ids=ids)
        # FORCE A PRINT TO PROVE IT WORKED
        print(f"DEBUG: Successfully saved {collection.count()} items to {DB_DIR}")
        return len(ids)
    return 0
