from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models, schemas

# Author CRUD
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

# Genre CRUD
def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

# Book CRUD
def create_book(db: Session, book: schemas.BookCreate):
    # Проверяем существование связей до создания записей
    if book.author_id is not None:
        get_or_404(db, models.Author, book.author_id, "Автор не найден")
    if book.publisher_id is not None:
        get_or_404(db, models.Publisher, book.publisher_id, "Издательство не найдено")
    for genre_id in book.genre_ids:
        get_or_404(db, models.Genre, genre_id, "Жанр не найден")

    # Создание нового автора
    if book.new_author:
        new_author = create_author(db, book.new_author)
        author_id = new_author.id
    else:
        author_id = book.author_id

    # Создание новых жанров с проверкой на дубликаты
    genre_ids = list(dict.fromkeys(book.genre_ids))
    if book.new_genres:
        seen = set()
        for genre_name in book.new_genres:
            key = genre_name.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            existing = db.query(models.Genre).filter(
                models.Genre.name == genre_name
            ).first()
            if existing:
                genre_ids.append(existing.id)
            else:
                genre_ids.append(create_genre(db, schemas.GenreCreate(name=genre_name)).id)

    db_book = models.Book(
        title=book.title,
        isbn=book.isbn,
        publication_year=book.publication_year,
        price=book.price,
        stock_quantity=book.stock_quantity,
        author_id=author_id,
        publisher_id=book.publisher_id
    )
    db.add(db_book)
    db.flush()

    # Добовление жанров
    for genre_id in genre_ids:
        book_genre = models.BookGenre(book_id=db_book.id, genre_id=genre_id)
        db.add(book_genre)

    commit_changes(db)
    db.refresh(db_book)
    return db_book, genre_ids

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


# Поиск книги по id
def get_book(db: Session, book_id: int):
    return get_or_404(db, models.Book, book_id, "Книга не найдена")


def get_or_404(db: Session, model, object_id: int, detail: str):
    obj = db.get(model, object_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=detail)
    return obj


def commit_changes(db: Session):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Операция нарушает целостность данных "
        ) from exc


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = get_or_404(db, models.Author, author_id, "Автор не найден")
    for key, value in author.model_dump(exclude_unset=True).items():
        setattr(db_author, key, value)
    commit_changes(db)
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_or_404(db, models.Author, author_id, "Автор не найден")
    if db.query(models.Book.id).filter(models.Book.author_id == author_id).first():
        raise HTTPException(status_code=409, detail="Нельзя удалить автора, у которого есть книги")
    db.delete(db_author)
    commit_changes(db)


def update_genre(db: Session, genre_id: int, genre: schemas.GenreUpdate):
    db_genre = get_or_404(db, models.Genre, genre_id, "Жанр не найден")
    for key, value in genre.model_dump(exclude_unset=True).items():
        setattr(db_genre, key, value)
    commit_changes(db)
    db.refresh(db_genre)
    return db_genre


def delete_genre(db: Session, genre_id: int):
    db_genre = get_or_404(db, models.Genre, genre_id, "Жанр не найден")
    db.delete(db_genre)
    commit_changes(db)


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = get_or_404(db, models.Book, book_id, "Книга не найдена")
    changes = book.model_dump(exclude_unset=True)
    if "isbn" in changes:
        existing = db.query(models.Book).filter(
            models.Book.isbn == changes["isbn"], models.Book.id != book_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")

    for field, model, detail in (
        ("author_id", models.Author, "Автор не найден"),
        ("publisher_id", models.Publisher, "Издательство не найдено"),
    ):
        if changes.get(field) is not None:
            get_or_404(db, model, changes[field], detail)

    # Проверка связей перед изменением записи
    genres = None
    if "genre_ids" in changes:
        genres = [
            get_or_404(db, models.Genre, genre_id, "Жанр не найден")
            for genre_id in dict.fromkeys(changes.pop("genre_ids"))
        ]
    for key, value in changes.items():
        setattr(db_book, key, value)
    if genres is not None:
        db_book.genres = genres
    commit_changes(db)
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_or_404(db, models.Book, book_id, "Книга не найдена")
    db.delete(db_book)
    commit_changes(db)