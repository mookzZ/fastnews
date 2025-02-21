"""
Main program module
"""

from fastapi import FastAPI

from src.news.routers.news import news_router
from src.news.routers.categories import category_router
from src.news.routers.comments import comment_router
from src.users.routers import users_router

app = FastAPI()

app.include_router(router=category_router)
app.include_router(router=news_router)
app.include_router(router=comment_router)
app.include_router(router=users_router)