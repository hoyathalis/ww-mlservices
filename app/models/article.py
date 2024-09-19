from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Dict, Optional

class Article(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None 
    url: Optional[str] = None 
    posted_at: Optional[date] = None  


class Interaction(BaseModel):
    article_id: str  
    like: int        
    dislike: int    
    interacted_at: Optional[datetime] = None  

