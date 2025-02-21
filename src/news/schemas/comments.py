from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CommentBase(BaseModel):
    """Base comment schema"""
    content: str
    news_id: int


class CommentCreate(CommentBase):
    """Create comment schema"""
    pass


class CommentUpdate(BaseModel):
    """Update comment schema"""
    content: str


class CommentRead(CommentBase):
    """Read comment schema"""
    id: int
    created: datetime
    updated: datetime
    user_id: UUID

    class Config:
        """Pydantic config"""
        from_attributes = True
