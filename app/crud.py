from sqlalchemy.orm import Session
from . import models, schemas

# === Author CRUD ===
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

# === Genre CRUD ===
def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

# === Book CRUD ===
def create_book(db: Session, book: schemas.BookCreate):
    # Создаем нового автора, если передан
    if book.new_author:
        new_author = create_author(db, book.new_author)
        author_id = new_author.id
    else:
        author_id = book.author_id

    # Создаем новые жанры, если переданы
    genre_ids = book.genre_ids.copy()
    if book.new_genres:
        for genre_name in book.new_genres:
            genre = schemas.GenreCreate(name=genre_name)
            new_genre = create_genre(db, genre)
            genre_ids.append(new_genre.id)

    # Создаем книгу (ИСПРАВЛЕНО: author_id вместо auther_id)
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

    # Добавляем жанры
    for genre_id in genre_ids:
        book_genre = models.BookGenre(book_id=db_book.id, genre_id=genre_id)
        db.add(book_genre)

    db.commit()
    db.refresh(db_book)
    return db_book, genre_ids

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()