from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime, Text, TIMESTAMP, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.exc import IntegrityError
import enum

# ==========================================
# 1. Настройка базы данных (SQLAlchemy)
# ==========================================
# Замените user, password, localhost и db_name на ваши реальные данные
DATABASE_URL = "mysql+pymysql://victoria:123@db:3306/mariadb"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 2. SQLAlchemy Модели (соответствуют вашей БД)
# ==========================================
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)

class Publisher(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)
    publication_year = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    stock_quantity = Column(Integer, nullable=False)
    
    # Внимание: в вашей БД опечатка "author_id", мы должны использовать её для маппинга
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
    publisher_id = Column(Integer, ForeignKey("publisher.id", ondelete="CASCADE"))

    # Relationships
    author = relationship("Author")
    publisher = relationship("Publisher")
    genres = relationship("Genre", secondary="book_genre", backref="books")

class BookGenre(Base):
    __tablename__ = "book_genre"
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)

# ==========================================
# 3. Pydantic Схемы (Валидация данных)
# ==========================================
class BookCreate(BaseModel):
    title: str
    isbn: str
    publication_year: int
    price: float
    stock_quantity: int
    author_id: int  # В API используем правильное написание
    publisher_id: int
    genre_ids: List[int] = []  # Список ID жанров

class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: int
    price: float
    stock_quantity: int
    author_id: int
    publisher_id: int
    genre_ids: List[int] = []

    # Настройка для Pydantic V2, чтобы он мог читать данные из SQLAlchemy моделей
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# 4. FastAPI Приложение и Эндпоинты
# ==========================================
app = FastAPI(title="Bookstore API")

@app.post("/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    # 1. Проверяем, нет ли уже книги с таким ISBN (так как в БД стоит UNIQUE)
    existing_book = db.query(Book).filter(Book.isbn == book_data.isbn).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга с таким ISBN уже существует"
        )

    # 2. Создаем объект книги
    # Маппим author_id из Pydantic в author_id из SQLAlchemy (исправляем опечатку БД)
    new_book = Book(
        title=book_data.title,
        isbn=book_data.isbn,
        publication_year=book_data.publication_year,
        price=book_data.price,
        stock_quantity=book_data.stock_quantity,
        author_id=book_data.author_id, 
        publisher_id=book_data.publisher_id
    )
    
    db.add(new_book)
    db.flush()  # Flush нужен, чтобы получить ID новой книги до коммита, но не закрывать транзакцию

    # 3. Добавляем жанры в связующую таблицу
    if book_data.genre_ids:
        # Проверяем, что все переданные жанры существуют (опционально, но полезно)
        existing_genres = db.query(Genre).filter(Genre.id.in_(book_data.genre_ids)).all()
        if len(existing_genres) != len(book_data.genre_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Один или несколько переданных genre_ids не существуют"
            )

        for genre_id in book_data.genre_ids:
            book_genre_link = BookGenre(book_id=new_book.id, genre_id=genre_id)
            db.add(book_genre_link)

    # 4. Сохраняем изменения в БД
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных. Убедитесь, что author_id и publisher_id существуют."
        )

    db.refresh(new_book)

    # 5. Формируем ответ
    response_data = BookResponse.model_validate(new_book)
    response_data.genre_ids = book_data.genre_ids
    
    return response_data

# Тестовый эндпоинт для проверки работоспособности
@app.get("/")
def read_root():
    return {"message": "API для книжного магазина работает!"}