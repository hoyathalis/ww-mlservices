# app/main.py

from fastapi import FastAPI
from app.api.api_v1.api import api_router

app = FastAPI(
    title="Article Recommendation Service",
    description="API for serving article recommendations",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")
