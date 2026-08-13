from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# === Author ===
class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None  # Добавлено
    bio_text: Optional[str] = None          # Добавлено

class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
    bio_text: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# === Genre ===
class GenreCreate(BaseModel):
    name: str

class GenreResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

# === Book ===
class BookCreate(BaseModel):
    title: str
    isbn: str
    publication_year: int
    price: float
    stock_quantity: int
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    genre_ids: List[int] = []
    new_author: Optional[AuthorCreate] = None
    new_genres: Optional[List[str]] = []

class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: int
    price: float
    stock_quantity: int
    author_id: Optional[int]
    publisher_id: Optional[int]
    genre_ids: List[int] = []
    model_config = ConfigDict(from_attributes=True)