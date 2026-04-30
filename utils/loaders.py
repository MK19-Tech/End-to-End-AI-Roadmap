from pypdf import PdfReader

def load_pdf(file_path):
    """Extracts text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_text(file):
    """Reads raw text or markdown files."""
    # Assuming 'file' is opened in binary mode 'rb' 
    return file.read().decode("utf-8")
