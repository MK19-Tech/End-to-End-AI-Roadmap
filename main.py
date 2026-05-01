import os
import glob
from utils.loaders import load_pdf, load_text
from utils.processors import clean_text
from utils.chunkers import chunk_text

def process_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    # 1. Extraction
    if ext == ".pdf":
        raw = load_pdf(file_path)
    elif ext in [".txt", ".md"]:
        raw = load_text(file_path)
    else:
        return None

    # 2. Cleaning (Step 3)
    cleaned = clean_text(raw)
    
    # 3. Chunking (Step 4)
    chunks = chunk_text(cleaned, chunk_size=500, overlap=100)
    return chunks

if __name__ == "__main__":
    files = sorted(glob.glob("data/sample*.*"))
    
    for file_path in files:
        chunks = process_document(file_path)
        if chunks:
            print(f"File: {os.path.basename(file_path)}")
            print(f"Created {len(chunks)} chunks.")
            print(f"First chunk: {chunks[0][:50]}...")
            print("-" * 25)
