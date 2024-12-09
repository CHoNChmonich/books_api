from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Author
from app.authors.authors_schemas import AuthorCreate
from typing import List, Optional


async def get_authors(db: AsyncSession) -> List[Author]:
    """Получить список всех авторов"""
    result = await db.execute(select(Author))
    return result.scalars().all()


async def get_author_by_id(author_id: int, db: AsyncSession) -> Optional[Author]:
    """Получить автора по id"""
    result = await db.execute(select(Author).where(Author.id == author_id))
    return result.scalar_one_or_none()


async def create_author(author: AuthorCreate, db: AsyncSession) -> Author:
    """Создать нового автора"""
    new_author = Author(**author.dict())
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author


async def update_author(author_id: int, author_data: AuthorCreate, db: AsyncSession) -> Optional[Author]:
    """Обновить данные автора"""
    author = await get_author_by_id(author_id, db)
    if not author:
        return None
    for field, value in author_data.dict().items():
        setattr(author, field, value)
    await db.commit()
    await db.refresh(author)
    return author


async def delete_author(author_id: int, db: AsyncSession) -> bool:
    """Удалить автора"""
    author = await get_author_by_id(author_id, db)
    if not author:
        return False
    await db.delete(author)
    await db.commit()
    return True