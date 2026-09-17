from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/genres", tags=["Genres"])

@router.post("/", response_model=schemas.GenreResponse, status_code=status.HTTP_201_CREATED)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    return crud.create_genre(db=db, genre=genre)

@router.get("/", response_model=List[schemas.GenreResponse])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    genres = crud.get_genres(db, skip=skip, limit=limit)
    return genres


@router.patch("/{genre_id}", response_model=schemas.GenreResponse)
def update_genre(genre_id: int, genre: schemas.GenreUpdate, db: Session = Depends(get_db)):
    return crud.update_genre(db, genre_id, genre)


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    crud.delete_genre(db, genre_id)