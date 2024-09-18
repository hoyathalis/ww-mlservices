from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Optional

class Article(BaseModel):
    id: Optional[str] = None
    
    #Mandatory
    title: str
    description: str
    tags: List[str] 
    url: str 

    posted_at: Optional[date] = None  
    metadata: Optional[Dict[str, str]] = None  


