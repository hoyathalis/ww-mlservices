from fastapi import APIRouter, HTTPException , status
from typing import List
from app.models.article import Article
from app.services.embedding_service import store_article_in_pinecone

router = APIRouter()


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def post_article(article: Article):
    """
    Create embeddings of the article and store it in Pinecone along with metadata.
    """
    try:
        store_article_in_pinecone(article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))