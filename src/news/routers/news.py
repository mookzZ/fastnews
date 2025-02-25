"""
Routers for news app
"""

from typing import Sequence, List
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
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
    title: str = Form(...),
    news_content: str | None = Form(default=None),
    category_id: int = Form(...),
    images: UploadFile | None = File(default=None),
    db: AsyncSession = Depends(get_async_session)
) -> News:
    """
    Create news with form data and images
    """
    saved_images = []
    if images:
        # Создаем уникальное имя файла
        file_name = f"{os.urandom(8).hex()}_{images.filename}"
        file_path = os.path.join("media", file_name)
        
        # Сохраняем файл
        file_content = await images.read()
        with open(file_path, "wb") as f:
            f.write(file_content)
        saved_images.append(file_name)  # Сохраняем только имя файла

    news_data = NewsCreate(
        title=title,
        content=news_content,
        category_id=category_id,
        images=saved_images if saved_images else None
    )
    
    return await NewsService.create_news(db, news_data)


@news_router.put("/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: int,
    title: str = Form(None),
    news_content: str = Form(None),
    category_id: int = Form(None),
    images: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_async_session)
) -> News:
    """
    Update news by id
    """
    news_data = NewsCreate(
        title=title,
        content=news_content,
        category_id=category_id,
        images=[images] if images else None
    )
    
    return await NewsService.update_news(db, news_id, news_data)


@news_router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    db: AsyncSession = Depends(get_async_session)
) -> None:
    """
    Delete news by id
    """
    return await NewsService.delete_news(db, news_id)
