from fastapi import FastAPI

from app.authors import authors_routes
from app.books import books_routes
from app.borrows import borrows_routes


app = FastAPI()

# Подключение маршрутов
app.include_router(authors_routes.router)
app.include_router(books_routes.router)
app.include_router(borrows_routes.router)
