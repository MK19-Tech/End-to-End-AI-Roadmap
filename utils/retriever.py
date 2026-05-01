import chromadb
from chromadb.utils import embedding_functions
import logging

def get_relevant_chunks(query, n_results=3, db_path="./chroma_db"):
    client = chromadb.PersistentClient(path=db_path)
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    try:
        # This will fail if main.py didn't complete its job
        collection = client.get_collection(name="my_documents", embedding_function=model)
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results["documents"][0] # Return the list of strings
    except Exception as e:
        # Provide a more helpful error message
        raise Exception("Collection 'my_documents' not found. Please run main.py again to index your files.")
