from fastapi import APIRouter, HTTPException , status
from typing import List
from app.models.article import Article
from app.services.recommendation_service import get_recommendations
from app.services.embedding_service import store_article_in_pinecone

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

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def post_article(article: Article):
    """
    Create embeddings of the article and store it in Pinecone along with metadata.
    """
    try:
        store_article_in_pinecone(article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))