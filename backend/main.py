from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routes import router
import logging

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug,
)

# CORS設定（フロントエンドからのリクエストを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを含める
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Pangaea Kaigi API - AI議論システム",
        "app_name": settings.app_name,
        "version": settings.api_version,
        "docs": "/docs",
    }
