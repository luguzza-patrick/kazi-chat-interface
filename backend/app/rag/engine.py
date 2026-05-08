import os
import faiss
import numpy as np
from typing import List, Dict
from starlette.concurrency import run_in_threadpool
from fastembed import TextEmbedding
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from app.core.config import settings

class RAGEngine:
    def __init__(self):
        self.model = TextEmbedding(model_name=settings.EMBEDDING_MODEL)
        self.index = None
        self.documents = []
        self._load_index()

    def _load_index(self):
        if os.path.exists(settings.FAISS_INDEX_PATH):
            self.index = faiss.read_index(os.path.join(settings.FAISS_INDEX_PATH, "index.faiss"))
            import json
            with open(os.path.join(settings.FAISS_INDEX_PATH, "docs.json"), "r") as f:
                self.documents = json.load(f)

    def ingest_file(self, file_path: str):
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        elif file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                text = f.read()
        else:
            raise ValueError("Unsupported file format")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(text)

        embeddings = list(self.model.embed(chunks))
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(chunks)

        self.save_index()

    def save_index(self):
        if not os.path.exists(settings.FAISS_INDEX_PATH):
            os.makedirs(settings.FAISS_INDEX_PATH)
        faiss.write_index(self.index, os.path.join(settings.FAISS_INDEX_PATH, "index.faiss"))
        import json
        with open(os.path.join(settings.FAISS_INDEX_PATH, "docs.json"), "w") as f:
            json.dump(self.documents, f)

    async def retrieve(self, query: str, k: int = 3) -> List[str]:
        if self.index is None:
            return []
        
        # Run heavy embedding and search in a thread pool to avoid blocking the event loop
        query_vector = await run_in_threadpool(lambda: list(self.model.embed([query]))[0])
        distances, indices = await run_in_threadpool(
            lambda: self.index.search(np.array([query_vector]).astype('float32'), k)
        )
        
        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.documents[idx])
        return results

rag_engine = RAGEngine()
