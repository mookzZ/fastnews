"""
Routers for news app
"""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.news.models import News
from src.news.schemas.news import NewsCreate, NewsRead
from src.news.services.news import NewsService

news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@news_router.get("", response_model=Sequence[NewsRead])
async def get_news_list(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
) -> Sequence[News]:
    """
    Get all news
    """
    return await NewsService.get_news_list(db, offset, limit)


@news_router.get("/{news_id}", response_model=NewsRead)
async def get_news(
    news_id: int,
    db: AsyncSession = Depends(get_async_session)
) -> News:
    """
    Get news by id
    """
    return await NewsService.get_news(db, news_id)


@news_router.post("", response_model=NewsRead)
async def create_news(
    news: NewsCreate,
    db: AsyncSession = Depends(get_async_session)
) -> News:
    """
    Create news
    """
    return await NewsService.create_news(db, news.dict())


@news_router.put("/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: int,
    news: NewsCreate,
    db: AsyncSession = Depends(get_async_session)
) -> News:
    """
    Update news by id
    """
    return await NewsService.update_news(db, news_id, news.dict())


@news_router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    db: AsyncSession = Depends(get_async_session)
) -> None:
    """
    Delete news by id
    """
    return await NewsService.delete_news(db, news_id)
