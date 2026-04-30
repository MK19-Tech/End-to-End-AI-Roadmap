import os
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
    content = process_document("data/sample.pdf")
    print(f"Extracted {len(content)} characters.")
