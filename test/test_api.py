import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app import models

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    test_session = sessionmaker(bind=engine)

    def get_test_db():
        with test_session() as db:
            yield db

    previous_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = get_test_db
    try:
        yield test_session
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
        engine.dispose()

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "API для книжного магазина работает!"


def test_create_and_list_author():
    author_data = {
        "first_name": "Тестовый",
        "last_name": "Автор",
        "birth_date": "0001-01-01T00:00:00.000Z",
        "bio_text": "Биография для теста"
    }

    create_resp = client.post("/authors/", json=author_data)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["first_name"] == author_data["first_name"]
    assert created["last_name"] == author_data["last_name"]
    assert "id" in created

    list_resp = client.get("/authors/")
    assert list_resp.status_code == 200
    authors = list_resp.json()
    assert any(a["id"] == created["id"] for a in authors)


def _create_author(first_name="Иван", last_name="Петров", bio_text=None):
    resp = client.post("/authors/", json={
        "first_name": first_name,
        "last_name": last_name,
        "bio_text": bio_text,
    })
    assert resp.status_code == 201
    return resp.json()


def _create_genre(name="Триллер"):
    resp = client.post("/genres/", json={"name": name})
    assert resp.status_code == 201
    return resp.json()


def _create_book(isbn="978-1-11", author_id=None, genre_ids=None, **overrides):
    data = {
        "title": "Тестовая книга",
        "isbn": isbn,
        "publication_year": 2020,
        "price": 100.0,
        "stock_quantity": 5,
    }
    if author_id is not None:
        data["author_id"] = author_id
    if genre_ids is not None:
        data["genre_ids"] = genre_ids
    data.update(overrides)
    resp = client.post("/books/", json=data)
    assert resp.status_code == 201, resp.text
    return resp.json()


# PATCH authors: отклонение в обязательных полях

def test_update_author_null_field_rejected():
    author = _create_author()
    resp = client.patch(f"/authors/{author['id']}", json={"last_name": None})
    assert resp.status_code == 422


# DELETE authors: защита от потери данных

def test_delete_author_with_books_forbidden():
    author = _create_author()
    _create_book(author_id=author["id"])

    resp = client.delete(f"/authors/{author['id']}")
    assert resp.status_code == 409
    assert client.get("/authors/").status_code == 200

# DELETE genres

def test_delete_genre_success_removes_link_from_books():
    genre = _create_genre("Детектив")
    book = _create_book(genre_ids=[genre["id"]])

    resp = client.delete(f"/genres/{genre['id']}")
    assert resp.status_code == 204

    # Книга осталась, связь с жанром удалена
    book_resp = client.get(f"/books/{book['id']}")
    assert book_resp.status_code == 200
    assert genre["id"] not in book_resp.json()["genre_ids"]


# PATCH books: частичное обновление

def test_update_book_success():
    book = _create_book()

    resp = client.patch(f"/books/{book['id']}", json={"title": "Новое название", "price": 250.50})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["title"] == "Новое название"
    assert updated["price"] == 250.5
    assert updated["isbn"] == book["isbn"]


def test_update_book_duplicate_isbn_forbidden():
    book_a = _create_book(isbn="978-A-1")
    _create_book(isbn="978-B-2")

    resp = client.patch(f"/books/{book_a['id']}", json={"isbn": "978-B-2"})
    assert resp.status_code == 400


# Замена и очистка жанров книги
def test_update_book_change_genres():
    g1 = _create_genre("Жанр 1")
    g2 = _create_genre("Жанр 2")
    book = _create_book(genre_ids=[g1["id"]])

    resp = client.patch(f"/books/{book['id']}", json={"genre_ids": [g2["id"]]})
    assert resp.status_code == 200
    assert resp.json()["genre_ids"] == [g2["id"]]

    # Пустой список очищает жанры
    resp = client.patch(f"/books/{book['id']}", json={"genre_ids": []})
    assert resp.status_code == 200
    assert resp.json()["genre_ids"] == []


# Обновление несуществующей книги
def test_update_book_not_found():
    assert client.patch("/books/99999", json={"title": "X"}).status_code == 404


# DELETE books

# Книга удалена, вместе с ней — связи в book_genre
def test_delete_book_success():
    book = _create_book()

    assert client.delete(f"/books/{book['id']}").status_code == 204
    assert client.get(f"/books/{book['id']}").status_code == 404