"""
Comments service module
"""
from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.news.models import Comment


class CommentService:
    """
    Service for managing comments
    """

    @staticmethod
    async def get_comments(
        db: AsyncSession,
        news_id: int | None = None,
        offset: int = 0,
        limit: int = 10
    ) -> Sequence[Comment]:
        """Get all comments"""
        query = select(Comment).offset(offset).limit(limit)
        if news_id:
            query = query.where(Comment.news_id == news_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_comment(db: AsyncSession, comment_id: int) -> Comment | None:
        """Get comment by id"""
        query = select(Comment).where(Comment.id == comment_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_comment(db: AsyncSession, data: dict, user_id: UUID) -> Comment:
        """Create new comment"""
        comment = Comment(**data, user_id=user_id)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def update_comment(
        db: AsyncSession,
        comment_id: int,
        data: dict,
        user_id: UUID
    ) -> Comment:
        """Update comment"""
        comment = await CommentService.get_comment(db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this comment")
        
        for key, value in data.items():
            setattr(comment, key, value)
        
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def delete_comment(db: AsyncSession, comment_id: int, user_id: UUID) -> None:
        """Delete comment"""
        comment = await CommentService.get_comment(db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
        
        await db.delete(comment)
        await db.commit()
