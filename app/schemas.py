from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime

class UpdateBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @field_validator("*", mode="before")
    @classmethod
    def reject_null_for_required_fields(cls, value, info):
        if value is None and info.field_name not in {"bio_text", "author_id", "publisher_id"}:
            raise ValueError("Поле не может быть null")
        return value


class AuthorUpdate(UpdateBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    bio_text: Optional[str] = None


class GenreUpdate(UpdateBase):
    name: Optional[str] = None


class BookUpdate(UpdateBase):
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None


# Author
class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
    bio_text: Optional[str] = None


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
    bio_text: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# Genre
class GenreCreate(BaseModel):
    name: str

class GenreResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

# Book
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