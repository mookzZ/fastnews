"""
Services module contains business logic
"""

from typing import Sequence
from datetime import datetime
import os

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from src.news.models import News, Comment
from src.news.schemas.news import NewsCreate
from src.manager import DBManager


class NewsService:
    @classmethod
    async def get_news_list(
        cls,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> Sequence[News]:
        """
        Get list of news
        """
        return await DBManager.get_objects(db, model=News, offset=offset, limit=limit)

    @classmethod
    async def get_news(
        cls,
        db: AsyncSession,
        news_id: int,
    ) -> News:
        """
        Get news by id
        """
        news = await DBManager.get_object(db=db, model=News, field="id", value=news_id)
        if news is None:
            raise HTTPException(status_code=404, detail="News not found")
        return news

    @classmethod
    async def create_news(
        cls,
        db: AsyncSession,
        news: NewsCreate,
    ) -> News:
        """
        Create news
        """
        news_dict = news.model_dump()
        return await DBManager.create_object(db=db, model=News, commit=True, **news_dict)

    @classmethod
    async def update_news(
        cls,
        db: AsyncSession,
        news_id: int,
        news_data: dict,
    ) -> News:
        """
        Update news
        """
        news = await cls.get_news(db, news_id)
        news_data["updated"] = datetime.utcnow()
        return await DBManager.update_object(db=db, obj=news, data=news_data)

    @classmethod
    async def delete_news(
        cls,
        db: AsyncSession,
        news_id: int,
    ) -> None:
        """
        Delete news and associated images and comments
        """
        # Получаем новость перед удалением
        news = await cls.get_news(db, news_id)
        
        # Удаляем связанные изображения
        if news.images:
            for image_path in news.images:
                try:
                    full_path = os.path.join("media", image_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                except Exception:
                    pass  # Игнорируем ошибки при удалении файлов
        
        # Сначала удаляем все комментарии к новости
        delete_comments = delete(Comment).where(Comment.news_id == news_id)
        await db.execute(delete_comments)
        await db.commit()
                    
        # Затем удаляем саму новость
        await DBManager.delete_object(db=db, model=News, field="id", value=news_id, commit=True)
