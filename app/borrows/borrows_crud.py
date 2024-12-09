from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Book, Borrow
from typing import List, Optional
from datetime import datetime
from app.borrows.borrows_schemas import BorrowReturn


# CRUD для Borrow
async def get_borrows(db: AsyncSession) -> List[Borrow]:
    """Получить список всех выдач"""
    result = await db.execute(select(Borrow))
    return result.scalars().all()


async def get_borrow_by_id(borrow_id: int, db: AsyncSession) -> Optional[Borrow]:
    """Получить запись о выдаче по id"""
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    return result.scalar_one_or_none()


async def create_borrow(borrow, db):
    # Удаление borrow_date из словаря, если он уже указан отдельно
    borrow_data = borrow.dict(exclude_unset=True)  # Оставляем только те поля, которые были заданы
    borrow_data['borrow_date'] = datetime.utcnow()  # Устанавливаем текущую дату
    new_borrow = Borrow(**borrow_data)
    db.add(new_borrow)
    await db.commit()
    await db.refresh(new_borrow)
    return new_borrow


async def return_borrow(borrow_id: int, return_data: BorrowReturn, db: AsyncSession):
    # Получаем запись о займе
    result = await db.execute(select(Borrow).filter_by(id=borrow_id))
    borrow = result.scalar_one_or_none()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    # Устанавливаем дату возврата
    borrow.return_date = datetime.now()

    # Получаем книгу, связанную с записью о займе
    result = await db.execute(select(Book).filter_by(id=borrow.book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Увеличиваем количество доступных экземпляров
    book.available_copies += 1

    # Сохраняем изменения в базе данных
    db.add_all([borrow, book])
    await db.commit()
    await db.refresh(borrow)  # Обновляем объект borrow, чтобы вернуть актуальные данные

    return borrow
