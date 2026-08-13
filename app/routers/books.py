from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Валидация: нельзя передавать и author_id, и new_author одновременно
    if book.author_id is not None and book.new_author is not None:
        raise HTTPException(
            status_code=400, 
            detail="Нельзя указать одновременно author_id и new_author. Выберите что-то одно."
        )
    
<<<<<<< HEAD
    # Валидация: нельзя передавать и genre_ids, и new_genres одновременно Вношу измененмия
=======
    # Валидация: нельзя передавать и genre_ids, и new_genres одновременно
>>>>>>> develop
    if book.genre_ids and book.new_genres:
        raise HTTPException(
            status_code=400,
            detail="Нельзя указать одновременно genre_ids и new_genres. Выберите что-то одно."
        )
    
    # Проверяем уникальность ISBN
    existing = db.query(crud.models.Book).filter(crud.models.Book.isbn == book.isbn).first()
    if existing:
        raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")
    
    db_book, genre_ids = crud.create_book(db=db, book=book)
    response = schemas.BookResponse.model_validate(db_book)
    response.genre_ids = genre_ids
    return response

@router.get("/", response_model=List[schemas.BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    result = []
    for book in books:
        response = schemas.BookResponse.model_validate(book)
        response.genre_ids = [g.id for g in book.genres]
        result.append(response)
    return result