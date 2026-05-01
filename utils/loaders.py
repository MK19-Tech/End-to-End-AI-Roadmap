from pypdf import PdfReader

def load_pdf(file_path):
    reader = PdfReader(file_path)
    return "".join([page.extract_text() or "" for page in reader.pages])

def load_text(file_path):
    with open(file_path, "rb") as f:
        return f.read().decode("utf-8")
