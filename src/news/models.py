from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.users.models import User


class Category(Base):
    """
    Category model
    """
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    news: Mapped[list["News"]] = relationship("News", back_populates="category")


class News(Base):
    """
    News model
    """
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=100), nullable=False)
    content: Mapped[str | None] = mapped_column(nullable=True)
    images: Mapped[list[str | None]] = mapped_column(ARRAY(String), nullable=True)
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="news")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="news")


class Comment(Base):
    """
    Comment model
    """
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(length=1000), nullable=False)
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    news = relationship("News", back_populates="comments")
    user = relationship("User", back_populates="comments")