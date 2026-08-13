import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, SessionLocal

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_db():
    def get_test_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()

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