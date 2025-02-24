"""
Module for database connection
"""

from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .environs import *

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=True)

class Base(DeclarativeBase):
    """
    Meta class for sqlalchemy ORM models
    """

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Coroutine for generating db session
    """
    async with async_session() as session:
        yield session

async def get_db() -> AsyncGenerator[Any, AsyncSession]:
    """
    Courutine for generating db session
    """
    async with async_session() as session:
        yield session


        # docker run --name dasifue_now -e POSTGRES_PASSWORD=123456 -p 6000:5432 -d postgres