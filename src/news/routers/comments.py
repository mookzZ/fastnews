from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.auth import current_active_user
from src.users.models import User
from src.news.models import Comment
from src.news.schemas.comments import CommentCreate, CommentRead, CommentUpdate
from src.news.services.comments import CommentService

comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


@comment_router.get("", response_model=Sequence[CommentRead])
async def get_comments(
    news_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
) -> Sequence[Comment]:
    """Get all comments, optionally filtered by news_id"""
    return await CommentService.get_comments(db, news_id, offset, limit)


@comment_router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_async_session)
) -> Comment:
    """Get comment by id"""
    comment = await CommentService.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@comment_router.post("", response_model=CommentRead)
async def create_comment(
    comment: CommentCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
) -> Comment:
    """Create new comment"""
    return await CommentService.create_comment(db, comment.dict(), user.id)


@comment_router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
) -> Comment:
    """Update comment"""
    return await CommentService.update_comment(db, comment_id, comment.dict(), user.id)


@comment_router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
) -> None:
    """Delete comment"""
    await CommentService.delete_comment(db, comment_id, user.id)
