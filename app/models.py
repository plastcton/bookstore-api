from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    birth_date = Column(DateTime, nullable=False, default='0000-00-00 00:00:00')
    bio_text = Column(Text, nullable=True)
    books = relationship("Book", back_populates="author")

class Publisher(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    founded_year = Column(Integer, nullable=False)

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    books = relationship("Book", secondary="book_genre", back_populates="genres")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)
    publication_year = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    stock_quantity = Column(Integer, nullable=False)
    # ИСПРАВЛЕНО: было auther_id, стало author_id
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
    publisher_id = Column(Integer, ForeignKey("publisher.id", ondelete="CASCADE"))

    author = relationship("Author", back_populates="books")
    publisher = relationship("Publisher")
    genres = relationship("Genre", secondary="book_genre", back_populates="books")

class BookGenre(Base):
    __tablename__ = "book_genre"
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)