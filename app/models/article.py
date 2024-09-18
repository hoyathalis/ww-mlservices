# app/models/article.py

from pydantic import BaseModel

class Article(BaseModel):
    id: int
    title: str
    url: str
    summary: str
