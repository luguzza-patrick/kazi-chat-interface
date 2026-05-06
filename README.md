# Kazi HR AI Agent

A production-structured HR AI agent with a FastAPI backend and a React frontend.

## Project Structure
- `backend/`: FastAPI server, PostgreSQL/SQLite DB, FAISS vector store.
- `frontend/`: React + Vite + TanStack Router chat interface.

## Quick Start

### 1. Prerequisites
- Python 3.12+ (managed by `uv`)
- Node.js & npm

### 2. Setup
```bash
# Setup backend
cd backend
make setup
make seed
make ingest

# Setup root dependencies (concurrently)
cd ..
npm install
```

### 3. Run Both (Frontend & Backend)
From the root directory:
```bash
npm run dev
```

## Individual Commands
- **Backend**: `cd backend && make run`
- **Frontend**: `cd frontend && npm run dev`
