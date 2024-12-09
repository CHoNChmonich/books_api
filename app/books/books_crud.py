from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Book
from app.books.books_schemas import BookCreate
from typing import List, Optional


# CRUD для Book
async def get_books(db: AsyncSession) -> List[Book]:
    """Получить список всех книг"""
    result = await db.execute(select(Book))
    return result.scalars().all()


async def get_book_by_id(book_id: int, db: AsyncSession) -> Optional[Book]:
    """Получить книгу по id"""
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def create_book(book: BookCreate, db: AsyncSession) -> Book:
    """Добавить новую книгу"""
    new_book = Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


async def update_book(book_id: int, book_data: BookCreate, db: AsyncSession) -> Optional[Book]:
    """Обновить данные книги"""
    book = await get_book_by_id(book_id, db)
    if not book:
        return None
    for field, value in book_data.dict().items():
        setattr(book, field, value)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(book_id: int, db: AsyncSession) -> bool:
    """Удалить книгу"""
    book = await get_book_by_id(book_id, db)
    if not book:
        return False
    await db.delete(book)
    await db.commit()
    return True