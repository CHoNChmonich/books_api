from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List


# Схемы для сущности Book
class BookBase(BaseModel):
    title: str
    description: Optional[str]
    author_id: int
    available_copies: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True