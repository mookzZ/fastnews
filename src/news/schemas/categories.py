"""
Pydantic schemas for news app
"""

from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    """
    Category base schema
    """
    name: str


class CategoryCreate(CategoryBase):
    """
    Category create schema
    """
    pass


class CategoryRead(CategoryBase):
    """
    Category read schema
    """
    id: int
    created: datetime

    class Config:
        from_attributes = True