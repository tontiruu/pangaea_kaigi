from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routes import router
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug,
)

# CORS configuration (allow requests from frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Pangaea Kaigi API - AI Discussion System",
        "app_name": settings.app_name,
        "version": settings.api_version,
        "docs": "/docs",
    }
