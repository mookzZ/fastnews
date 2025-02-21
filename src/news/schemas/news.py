"""
Pydantic schemas for news app
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class NewsBase(BaseModel):
    """
    Base news schema
    """
    title: str
    content: Optional[str] = None
    images: Optional[List[str]] = None
    category_id: int


class NewsCreate(NewsBase):
    """
    News create schema
    """
    pass


class NewsRead(NewsBase):
    """
    News read schema
    """
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True
