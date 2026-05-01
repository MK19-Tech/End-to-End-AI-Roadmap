import os
import glob
import re
import unicodedata
from pypdf import PdfReader

def clean_text(text):
    """Logic from Image Step 3: Clean and preprocess"""
    # 1. Normalize unicode (Optional improvement from image)
    # This fixes issues like curly quotes or accented characters
    text = unicodedata.normalize('NFKD', text)
    
    # 2. Core cleaning logic from image
    # Replaces multiple whitespaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # 3. Final trim
    return text.strip()

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_text(file_object):
    return file_object.read().decode("utf-8")

def process_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    # Extract raw text
    if ext == ".pdf":
        raw_text = load_pdf(file_path)
    elif ext in [".txt", ".md"]:
        with open(file_path, "rb") as f:
            raw_text = load_text(f)
    else:
        return None

    # Clean the text before returning (Step 3 integration)
    return clean_text(raw_text)

if __name__ == "__main__":
    # Path to search
    data_path = os.path.join("data", "sample*.*")
    matching_files = sorted(glob.glob(data_path))

    processed_count = 0
    for file_path in matching_files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".pdf", ".txt", ".md"]:
            content = process_document(file_path)
            
            if content:
                print(f"File: {os.path.basename(file_path)}")
                print(f"Cleaned Length: {len(content)} characters.")
                print(f"Snippet: {content[:50]}...") # Verify cleaning
                print("-" * 25)
                processed_count += 1
        
    if processed_count == 0:
        print("No supported files found in the 'data/' folder.")
