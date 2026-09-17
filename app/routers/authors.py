from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", response_model=schemas.AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@router.get("/", response_model=List[schemas.AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@router.patch("/{author_id}", response_model=schemas.AuthorResponse)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    return crud.update_author(db, author_id, author)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    crud.delete_author(db, author_id)