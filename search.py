import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from utils.retriever import get_relevant_chunks

if __name__ == "__main__":
    print("\n--- RAG Retrieval System Ready ---")
    user_query = input("Ask a question about your documents: ")
    
    if not user_query.strip():
        print("Empty query. Exiting.")
    else:
        try:
            relevant_chunks = get_relevant_chunks(user_query, n_results=3)
            
            print(f"\nTop {len(relevant_chunks)} Results Found:")
            for i, chunk in enumerate(relevant_chunks, 1):
                print(f"\n[{i}] {chunk[:400]}...") 
                print("-" * 30)
                
        except Exception as e:
            print(f"\n[ERROR] {e}")
