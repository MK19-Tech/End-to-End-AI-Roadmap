import os
import glob
import logging
from utils.loaders import load_pdf, load_text
from utils.processors import clean_text
from utils.chunkers import chunk_text

# --- CONFIGURATION ---
CHUNK_SIZE = 750
CH_OVERLAP = 150
DATA_FOLDER = "data"
LOG_FILE = "processing.log"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE), # Saves to file
            logging.StreamHandler()        # Prints to terminal
        ]
    )

def process_pipeline(file_path, size, overlap):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        # 1. Extraction
        if ext == ".pdf":
            raw = load_pdf(file_path)
        elif ext in [".txt", ".md"]:
            raw = load_text(file_path)
        else:
            logging.warning(f"Skipping: {file_path} (Unsupported format)")
            return None

        # 2. Cleaning
        cleaned = clean_text(raw)
        
        # 3. Chunking
        chunks = chunk_text(cleaned, chunk_size=size, overlap=overlap)
        logging.info(f"Processed {os.path.basename(file_path)}: {len(chunks)} chunks created.")
        return chunks

    except Exception as e:
        logging.error(f"Failed to process {file_path}: {str(e)}")
        return None

if __name__ == "__main__":
    setup_logging()
    logging.info("--- Starting Document Processing Pipeline ---")
    
    search_path = os.path.join(DATA_FOLDER, "sample*.*")
    files = sorted(glob.glob(search_path))
    
    if not files:
        logging.info("No files found to process.")
    
    for file_path in files:
        process_pipeline(file_path, CHUNK_SIZE, CH_OVERLAP)

    logging.info("--- Pipeline Finished ---")
