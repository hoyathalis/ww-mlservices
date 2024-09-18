# app/api/api_v1/endpoints/recommendations.py

from fastapi import APIRouter, HTTPException
from typing import List
from app.models.article import Article
from app.services.recommendation_service import get_recommendations

router = APIRouter()

@router.get("/", response_model=List[Article])
async def read_recommendations(user_id: int):
    """
    Retrieve article recommendations for a given user ID.
    """
    recommendations = get_recommendations(user_id)
    if not recommendations:
        raise HTTPException(status_code=404, detail="Recommendations not found")
    return recommendations
