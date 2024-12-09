from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List


class BorrowBase(BaseModel):
    book_id: int
    borrower_name: str
    borrow_date: datetime


class BorrowCreate(BorrowBase):
    pass


class BorrowReturn(BaseModel):
    return_date: datetime


class BorrowResponse(BorrowBase):
    id: int
    return_date: Optional[datetime]

    class Config:
        orm_mode = True