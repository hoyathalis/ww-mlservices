# app/api/api_v1/api.py

from fastapi import APIRouter
from app.api.api_v1.endpoints import recommendations

api_router = APIRouter()
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"]
)
