#!/bin/bash
set -e

echo "--- Starting Kazi HR Backend Setup ---"

# 1. Seed the database with employees and payroll data
echo "Seeding database..."
uv run python scripts/seed_db.py

# 2. Ingest PDFs and TXT files for the RAG system
echo "Ingesting HR documents..."
uv run python scripts/ingest_data.py

# 3. Start the FastAPI server
echo "Starting server on port 8080..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
