import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.engine import RAGEngine
from app.core.config import settings

def ingest():
    # Check if FAISS index files actually exist
    index_path = os.path.join(settings.FAISS_INDEX_PATH, "index.faiss")
    docs_path = os.path.join(settings.FAISS_INDEX_PATH, "docs.json")
    
    if os.path.exists(index_path) and os.path.exists(docs_path):
        print("Documents already ingested. Skipping...")
        return

    # Create a fresh RAG engine instance for ingestion
    rag_engine = RAGEngine()
    
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
