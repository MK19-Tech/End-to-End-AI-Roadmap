import os
# Silences the Symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# Silences the unauthenticated request warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import logging
from utils.retriever import get_relevant_chunks

if __name__ == "__main__":
    print("--- RAG Retrieval System Ready ---")
    user_query = input("Ask a question about your documents: ")
    
    # Execute Step 7 logic
    try:
        relevant_chunks = get_relevant_chunks(user_query, n_results=3)
        
        print(f"\nFound {len(relevant_chunks)} relevant sections:\n")
        for i, chunk in enumerate(relevant_chunks, 1):
            print(f"--- Result {i} ---")
            print(f"{chunk[:300]}...") # Show first 300 chars
            print("-" * 20)
            
    except Exception as e:
        print(f"Make sure you've run main.py first! Error: {e}")
