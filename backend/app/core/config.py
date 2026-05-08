from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Kazi HR AI Agent"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/kazi"
    DEV_MODE: bool = True
    SQLITE_URL: str = "sqlite:///./kazi.db"

    # LLM Providers
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    LLM_MODEL: str = "deepseek-chat"
    
    # RAG
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    FAISS_INDEX_PATH: str = "data/faiss_index"
    PDF_DATA_PATH: str = "data/pdfs"

    # Static Files
    STATIC_DIR: str = "static"

    class Config:
        env_file = ".env"

settings = Settings()
