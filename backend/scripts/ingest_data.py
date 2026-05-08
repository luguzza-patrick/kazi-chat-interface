import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.engine import rag_engine

def ingest():
    # Skip if already ingested
    if rag_engine.documents:
        print("Documents already ingested. Skipping...")
        return

    data_dir = "data/pdfs"
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} not found. Skipping...")
        return
        
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.endswith((".pdf", ".txt")):
            print(f"Ingesting {filename}...")
            rag_engine.ingest_file(file_path)
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest()
