from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.books.books_schemas import BookCreate, BookResponse
from app.books.books_crud import (
    get_books,
    get_book_by_id,
    create_book,
    update_book,
    delete_book,
)
from app.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse])
async def list_books(db: AsyncSession = Depends(get_db)):
    """
    Получить список всех книг.
    """
    books = await get_books(db)
    return books


@router.get("/{book_id}", response_model=BookResponse)
async def retrieve_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить книгу по ID.
    """
    book = await get_book_by_id(book_id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=201)
async def create_new_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    """
    Добавить новую книгу.
    """
    new_book = await create_book(book, db)
    return new_book


@router.put("/{book_id}", response_model=BookResponse)
async def update_existing_book(
        book_id: int, book_data: BookCreate, db: AsyncSession = Depends(get_db)
):
    """
    Обновить данные книги.
    """
    updated_book = await update_book(book_id, book_data, db)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/{book_id}", status_code=204)
async def delete_existing_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить книгу по ID.
    """
    success = await delete_book(book_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return
