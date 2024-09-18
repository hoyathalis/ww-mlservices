# app/services/recommendation_service.py

from typing import List
from app.models.article import Article

def get_recommendations(user_id: int) -> List[Article]:
    """
    Mock function to get article recommendations for a user.
    Replace this with your actual recommendation logic.
    """
    # Mock data
    articles = [
        Article(
            id=1,
            title="Understanding FastAPI",
            url="https://example.com/fastapi",
            summary="An introduction to FastAPI framework.",
        ),
        Article(
            id=2,
            title="Advanced Python Tips",
            url="https://example.com/python-tips",
            summary="Improve your Python skills with these tips.",
        ),
    ]
    return articles
