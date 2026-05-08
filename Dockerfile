# --- Stage 1: Build Frontend ---
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Build the frontend as a static SPA
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Build Backend ---
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin/:$PATH"

# Copy backend dependency files
COPY backend/pyproject.toml backend/uv.lock ./backend/
WORKDIR /app/backend

# Install backend dependencies
RUN uv sync --no-dev && rm -rf /root/.cache/uv

# Pre-download embedding model to prevent freezing on startup
RUN . .venv/bin/activate && python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='sentence-transformers/all-MiniLM-L6-v2')"

# Copy backend source
COPY backend/ ./

# Copy frontend build from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/backend/static

# Make startup script executable
RUN chmod +x start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STATIC_DIR=static
ENV PORT=8080

# Expose port
EXPOSE 8080

# Command to run the application
CMD ["./start.sh"]
