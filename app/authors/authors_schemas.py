from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List


# Схемы для сущности Author
class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[date]


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int

    class Config:
        orm_mode = True