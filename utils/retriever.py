import chromadb
from chromadb.utils import embedding_functions

def get_relevant_chunks(query, n_results=3, db_path="./chroma_db"):
    """Implements Step 7: Retrieval logic from image"""
    client = chromadb.PersistentClient(path=db_path)
    
    # Must use the same 'meaning maker' model as we did in Step 6
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.get_collection(name="my_documents", embedding_function=model)
    
    # This matches the 'index.search' logic from your image
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Return the 'relevant_chunks' (documents) as a list
    return results["documents"][0]
