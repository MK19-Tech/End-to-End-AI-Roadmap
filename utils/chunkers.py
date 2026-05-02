def chunk_text(text, chunk_size=500, overlap=100):
    """Chunking logic from Image Step 4"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
