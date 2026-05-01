import chromadb
from chromadb.utils import embedding_functions

# Connect to the same folder
client = chromadb.PersistentClient(path="./chroma_db")
model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_collection(name="my_documents", embedding_function=model)

# Ask a question!
results = collection.query(
    query_texts=["What does the document say about sample topics?"],
    n_results=2 # Give me the top 2 best matches
)

print(results["documents"])
