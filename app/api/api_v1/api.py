# app/api/api_v1/api.py

from fastapi import APIRouter
from app.api.api_v1.endpoints import recommendations
from app.api.api_v1.endpoints.embeddings import article


api_router = APIRouter()
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"] 
)
api_router.include_router(
    article.router, prefix="/embeddings/article", tags=["embeddings"]    
    
)
