import os
import glob
import logging
# Silences the Symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from utils.loaders import load_pdf, load_text
from utils.processors import clean_text
from utils.chunkers import chunk_text
from utils.savers import save_chunks_to_json
from utils.vector_store import add_to_vector_db 

# --- CONFIG ---
CHUNK_SIZE = 750
CH_OVERLAP = 150
DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"
LOG_FILE = "processing.log"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
    )

def process_pipeline(file_path):
    file_name = os.path.basename(file_path)
    try:
        # 1. Extract
        ext = os.path.splitext(file_path)[1].lower()
        raw = load_pdf(file_path) if ext == ".pdf" else load_text(file_path)
        
        # 2. Clean & Chunk
        cleaned = clean_text(raw)
        chunks = chunk_text(cleaned, CHUNK_SIZE, CH_OVERLAP)
        
        # 3. Save to JSON (For backup/inspection)
        save_chunks_to_json(file_name, chunks, OUTPUT_FOLDER)
        
        # 4. Add to Vector DB
        count = add_to_vector_db(chunks, file_name)
        
        logging.info(f"Success: {file_name} -> {count} vectors stored.")
    except Exception as e:
        logging.error(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    setup_logging()
    # Find all files in data folder
    files = sorted(glob.glob(os.path.join(DATA_FOLDER, "*.*")))
    
    if not files:
        print(f"No files found in {DATA_FOLDER}!")
    else:
        for f in files:
            process_pipeline(f)
