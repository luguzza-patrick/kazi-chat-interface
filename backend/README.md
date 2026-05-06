# Kazi HR AI Agent Backend

Kazi is a production-structured HR AI agent built with FastAPI, PostgreSQL, and FAISS.

## Features
- **RAG (Retrieval-Augmented Generation)**: Answers HR policy questions using PDF/TXT documents.
- **RBAC (Role-Based Access Control)**: Strictly enforces data isolation using NetworkX graphs.
- **Pluggable LLM**: Supports DeepSeek and other providers.
- **Employee Data**: Retrieves leave and payroll information from a secure DB.

## Tech Stack
- **FastAPI**: Backend framework
- **PostgreSQL**: Production database (SQLite for development)
- **SQLAlchemy**: ORM
- **NetworkX**: Access control graph
- **FAISS**: Vector database for RAG
- **Sentence Transformers**: Text embeddings

## Setup

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Set up Environment**
   Create a `.env` file:
   ```env
   DEEPSEEK_API_KEY=your_key_here
   DEV_MODE=True
   ```

3. **Initialize Database and RAG**
   ```bash
   make seed
   make ingest
   ```

4. **Run the Server**
   ```bash
   make run
   ```

## Makefile Commands
- `make setup`: Install dependencies.
- `make run`: Start the FastAPI server.
- `make seed`: Seed the database with dummy data.
- `make ingest`: Ingest PDF/TXT policies into FAISS.
- `make test`: Run pytest suite.
- `make clean`: Remove database and index files.
- **Endpoint**: `POST /api/v1/chat`
- **Payload**:
  ```json
  {
    "user_id": 1,
    "message": "How many leave days do I have left?"
  }
  ```

## Testing
```bash
PYTHONPATH=. uv run pytest tests/
```
