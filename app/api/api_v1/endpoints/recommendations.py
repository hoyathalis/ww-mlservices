from fastapi import APIRouter, HTTPException , status
from typing import List
from app.models.article import Article , Interaction
from app.services.recommendation_service import fetch_recommendations

router = APIRouter()

@router.post("/", response_model=List[Article])
async def read_recommendations(interactions: List[Interaction]):
    """

    Retrieve article recommendations for a given user ID.
    """
    recommendations = fetch_recommendations(interactions) 
    if not recommendations:
        raise HTTPException(status_code=404, detail="Recommendations not found")
    return recommendations


