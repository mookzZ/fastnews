from .routers.news import news_router
from .routers.categories import category_router
from .routers.comments import comment_router

__all__ = [
    "news_router",
    "category_router",
    "comment_router",
]