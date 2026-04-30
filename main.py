import os
import glob
from utils.loaders import load_pdf, load_text

def process_document(file_path):
    # Get the file extension (.pdf, .txt, etc.)
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext in [".txt", ".md"]:
        with open(file_path, "rb") as f:
            return load_text(f)
    else:
        return "Unsupported file format"

# Example Usage
if __name__ == "__main__":
    # 1. Find all files that match the pattern (sample1.pdf, sample2.pdf, etc.)
    # Use sorted() to ensure they are processed in order (1, 2, 3...)
    matching_files = sorted(glob.glob("data/sample*.pdf"))

    # 2. Iterate through each file one by one
    for file_path in matching_files:
        content = process_document(file_path)
        
        # 3. Print results for the specific file being processed
        print(f"File: {os.path.basename(file_path)}")
        print(f"Extracted {len(content)} characters.")
        print("-" * 20)
        
    if not matching_files:
        print("No files matching 'sample*.pdf' found in the data directory.")
