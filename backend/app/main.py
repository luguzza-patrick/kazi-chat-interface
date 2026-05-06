from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.db.session import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Kazi HR AI Agent API"}
