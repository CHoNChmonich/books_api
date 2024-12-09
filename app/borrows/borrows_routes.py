from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.borrows.borrows_schemas import BorrowCreate, BorrowResponse, BorrowReturn
from app.borrows.borrows_crud import (
    get_borrows,
    get_borrow_by_id,
    create_borrow,
    return_borrow
)
from app.database import get_db

router = APIRouter(prefix="/borrows", tags=["Borrows"])


@router.get("/", response_model=List[BorrowResponse])
async def list_borrows(db: AsyncSession = Depends(get_db)):
    """
    Получить список всех записей о выдаче.
    """
    borrows = await get_borrows(db)
    return borrows


@router.get("/{borrow_id}", response_model=BorrowResponse)
async def retrieve_borrow(borrow_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить запись о выдаче книги по ID.
    """
    borrow = await get_borrow_by_id(borrow_id, db)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return borrow


@router.post("/", response_model=BorrowResponse, status_code=201)
async def create_new_borrow(borrow: BorrowCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новую запись о выдаче книги.
    Проверяет наличие доступных экземпляров книги перед выдачей.
    """
    new_borrow = await create_borrow(borrow, db)
    if not new_borrow:
        raise HTTPException(status_code=400, detail="No available copies of the book")
    return new_borrow


@router.patch("/{borrow_id}/return", response_model=BorrowResponse)
async def return_borrowed_book(
    borrow_id: int, return_data: BorrowReturn, db: AsyncSession = Depends(get_db)
):
    """
    Завершить выдачу книги, указав дату возврата.
    Увеличивает количество доступных экземпляров книги.
    """
    updated_borrow = await return_borrow(borrow_id, return_data, db)
    return updated_borrow

