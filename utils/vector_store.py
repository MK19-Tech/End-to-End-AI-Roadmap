import chromadb
from chromadb.utils import embedding_functions

def add_to_vector_db(chunks, source_name, db_path="./chroma_db"):
    # 1. Initialize the local database
    client = chromadb.PersistentClient(path=db_path)
    
    # 2. Choose a "meaning maker" (Embedding Function)
    # This runs locally on your CPU
    model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Create or get a "Collection" (like a folder in the DB)
    collection = client.get_or_create_collection(name="my_documents", embedding_function=model)
    
    # 4. Prepare data for the DB
    ids = [f"{source_name}_{i}" for i in range(len(chunks))]
    metadata = [{"source": source_name} for _ in range(len(chunks))]
    
    # 5. Add to database
    collection.add(
        documents=chunks,
        metadatas=metadata,
        ids=ids
    )
    return len(ids)
