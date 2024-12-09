from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Author(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    available_copies = Column(Integer, nullable=False, default=1)

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, available_copies={self.available_copies})>"


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    borrower_name = Column(String, nullable=False)
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="borrows")

    def __repr__(self):
        return f"<Borrow(id={self.id}, book_id={self.book_id}, borrower_name={self.borrower_name})>"
