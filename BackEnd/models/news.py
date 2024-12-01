from pydantic import BaseModel
from typing import List

class NewsItem(BaseModel):
    company: str
    news_content: str
    summary: str
    datetime: str

class NewsResponse(BaseModel):
    data: List[NewsItem]
