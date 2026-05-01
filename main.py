import os
import glob
from pypdf import PdfReader  # Ensure pypdf is installed: pip install pypdf

def load_pdf(file_path):
    """Extraction logic from image Step 2: PDF extraction"""
    # Note: Opening the file path directly is often more stable than 
    # passing a generic file object for PDFs.
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        # Image logic: extraction with fallback to empty string
        text += page.extract_text() or ""
    return text

def load_text(file_object):
    """Extraction logic from image Step 2: Text/Markdown"""
    # Image logic: reading and decoding as utf-8
    return file_object.read().decode("utf-8")

def process_document(file_path):
    # Get the file extension (.pdf, .txt, etc.)
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext in [".txt", ".md"]:
        # Image uses binary read 'rb' before decoding
        with open(file_path, "rb") as f:
            return load_text(f)
    else:
        return "Unsupported file format"

if __name__ == "__main__":
    # Updated to find PDFs, Text, and Markdown files as per image requirements
    # Looking for any 'sample' file in the 'data' directory
    matching_files = sorted(glob.glob("data/sample*.*"))

    processed_count = 0
    for file_path in matching_files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".pdf", ".txt", ".md"]:
            content = process_document(file_path)
            
            print(f"File: {os.path.basename(file_path)}")
            print(f"Extracted {len(content)} characters.")
            print("-" * 25)
            processed_count += 1
        
    if processed_count == 0:
        print("No supported files (PDF, TXT, MD) found matching 'sample*' in the data directory.")
