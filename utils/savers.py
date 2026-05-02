import json
import os

def save_chunks_to_json(file_name, chunks, output_folder="output"):
    """Saves chunks as a structured JSON file."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Create a safe filename for the JSON
    base_name = os.path.splitext(file_name)[0]
    output_path = os.path.join(output_folder, f"{base_name}_chunks.json")
    
    data = {
        "source_file": file_name,
        "total_chunks": len(chunks),
        "chunks": [{"id": i, "content": text} for i, text in enumerate(chunks)]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return output_path
