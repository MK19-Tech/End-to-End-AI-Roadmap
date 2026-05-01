import os
import glob
import logging
from utils.loaders import load_pdf, load_text
from utils.processors import clean_text
from utils.chunkers import chunk_text
from utils.savers import save_chunks_to_json # New Import

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
        
        # 3. Save (New Step!)
        save_path = save_chunks_to_json(file_name, chunks, OUTPUT_FOLDER)
        
        logging.info(f"Success: {file_name} -> {len(chunks)} chunks saved to {save_path}")
    except Exception as e:
        logging.error(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    setup_logging()
    files = sorted(glob.glob(os.path.join(DATA_FOLDER, "sample*.*")))
    
    for f in files:
        process_pipeline(f)
