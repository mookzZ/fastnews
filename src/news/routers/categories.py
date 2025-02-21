"""
Routers for news app
"""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.news.models import Category
from src.news.schemas.categories import CategoryCreate, CategoryRead
from src.news.services.categories import CategoryService


category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@category_router.get("", response_model=Sequence[CategoryRead])
async def get_categories(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)) -> Sequence[Category]:
    """
    Get all categories
    """
    return await CategoryService.get_categories(db, offset, limit)


@category_router.get("/{category_id}", response_model=CategoryRead)
async def get_category(category_id: int, db: AsyncSession = Depends(get_async_session)) -> Category:
    """
    Get category by id
    """
    return await CategoryService.get_category(db, category_id)


@category_router.post("", response_model=CategoryRead)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_async_session)) -> Category:
    """
    Create category
    """
    return await CategoryService.create_category(db, category.dict())


@category_router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    """
    Delete category by id
    """
    return await CategoryService.delete_category(db, category_id)


@category_router.put("/{category_id}", response_model=CategoryRead)
async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_async_session)) -> Category:
    """
    Update category by id
    """
    return await CategoryService.update_category(db, category_id, category.dict())


@category_router.patch("/{category_id}", response_model=CategoryRead)
async def partial_update_category(category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_async_session)) -> Category:
    """
    Update category by id
    """
    return await CategoryService.update_category(db, category_id, category.dict(), partial=True)
