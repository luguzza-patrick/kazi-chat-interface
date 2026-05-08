.PHONY: setup run ingest seed test clean

setup:
	uv sync

run: seed ingest
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

ingest:
	uv run python scripts/ingest_data.py

seed:
	uv run python scripts/seed_db.py

test:
	PYTHONPATH=. uv run pytest tests/

clean:
	rm -rf data/faiss_index kazi.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
