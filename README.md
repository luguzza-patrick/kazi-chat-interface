# Kazi HR AI Agent

Kazi is an AI-powered HR assistant designed to help employees and HR teams with policy information, leave management, payroll queries, and more.

## Deployment to Render (Single Container)

This project is configured for single-container deployment on Render.

### Prerequisites

1. A [Render](https://render.com) account.
2. A DeepSeek API Key (or a compatible OpenAI-style API endpoint).

### Steps

1. **Create a New Web Service**:
   - Choose **Deploy an existing image** or **Connect your GitHub repository**.
   - If connecting via GitHub, Render will automatically detect the `Dockerfile`.

2. **Configure Environment Variables**:
   Add the following variables in the Render dashboard:
   - `DEEPSEEK_API_KEY`: Your API key.
   - `DEEPSEEK_BASE_URL`: (Optional) Defaults to `https://api.deepseek.com/v1`. Change this if using a custom model endpoint.
   - `LLM_MODEL`: (Optional) Defaults to `deepseek-chat`.
   - `DATABASE_URL`: (Optional) Defaults to `sqlite:///./kazi.db`. For production, use a Render Managed PostgreSQL instance.
   - `PORT`: `8000` (Render sets this automatically, but ensure it matches).

3. **Deploy**:
   - Render will build the multi-stage Dockerfile (Frontend build + Backend setup) and serve everything on port 8000.

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
