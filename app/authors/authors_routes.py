from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.authors.authors_schemas import AuthorCreate, AuthorResponse
from app.authors.authors_crud import get_authors, get_author_by_id, delete_author, update_author, create_author
from app.database import get_db

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[AuthorResponse])
async def list_authors(db: AsyncSession = Depends(get_db)):
    """
    Получить список всех авторов.
    """
    authors = await get_authors(db)
    return authors


@router.get("/{author_id}", response_model=AuthorResponse)
async def retrieve_author(author_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить автора по ID.
    """
    author = await get_author_by_id(author_id, db)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/", response_model=AuthorResponse, status_code=201)
async def create_new_author(author: AuthorCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать нового автора.
    """
    new_author = await create_author(author, db)
    return new_author


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_existing_author(
    author_id: int, author_data: AuthorCreate, db: AsyncSession = Depends(get_db)
):
    """
    Обновить информацию об авторе.
    """
    updated_author = await update_author(author_id, author_data, db)
    if not updated_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@router.delete("/{author_id}", status_code=204)
async def delete_existing_author(author_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить автора по ID.
    """
    success = await delete_author(author_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Author not found")
    return
