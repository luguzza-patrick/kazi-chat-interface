from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.db.session import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Serve static files if directory exists
if os.path.exists(settings.STATIC_DIR):
    # Mount assets directory for direct serving
    assets_dir = os.path.join(settings.STATIC_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # 1. Check if the path points to an actual file in settings.STATIC_DIR
        file_path = os.path.join(settings.STATIC_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # 2. Prevent API routes from being swallowed by the catch-all
        if full_path.startswith(settings.API_V1_STR.lstrip("/")):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API route not found")
        
        # 3. Default to index.html for SPA routing
        index_path = os.path.join(settings.STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"detail": "Static files not found"}
else:
    @app.get("/")
    async def root():
        return {"message": "Welcome to Kazi HR AI Agent API (Static files not found)"}
