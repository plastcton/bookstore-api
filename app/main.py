from fastapi import FastAPI
from .routers import books, authors, genres

app = FastAPI(title="Bookstore API")

# Подключение роутеров
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)

@app.get("/")
def read_root():
    return {"message": "API для книжного магазина работает!"}