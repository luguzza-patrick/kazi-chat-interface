# Kazi HR AI Agent

A production-structured HR AI agent with a FastAPI backend and a React frontend.

## Project Structure
- `backend/`: FastAPI server, PostgreSQL/SQLite DB, FAISS vector store.
- `frontend/`: React + Vite + TanStack Router chat interface.

## Quick Start

### 1. Prerequisites
- Python 3.12+ (managed by `uv`)
- Node.js & npm

### 2. Authentication
Access the system using the test credentials found in [credentials.txt](credentials.txt). The dropdown for user switching has been replaced by a login system for enhanced security and realistic simulation.

### 3. Setup
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
