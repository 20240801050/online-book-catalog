
import pytest
import app as book_app


@pytest.fixture
def client(tmp_path):
    book_app.DATABASE = str(tmp_path / "test_books.db")
    book_app.app.config["TESTING"] = True
    book_app.init_db()

    with book_app.app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Online Book Catalog" in response.data


def test_add_book(client):
    response = client.post("/add", data={
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "isbn": "9780061122415",
        "genre": "Fiction",
        "year": "1988"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"The Alchemist" in response.data


def test_duplicate_isbn(client):
    book_data = {
        "title": "Book One",
        "author": "Author One",
        "isbn": "123456789",
        "genre": "Fiction",
        "year": "2020"
    }

    client.post("/add", data=book_data)
    response = client.post("/add", data=book_data, follow_redirects=True)

    assert b"ISBN already exists" in response.data or b"ISBN" in response.data


def test_search_book(client):
    client.post("/add", data={
        "title": "Python Basics",
        "author": "John Smith",
        "isbn": "987654321",
        "genre": "Technology",
        "year": "2022"
    })

    response = client.get("/?search=Python")
    assert response.status_code == 200
    assert b"Python Basics" in response.data


def test_delete_book(client):
    client.post("/add", data={
        "title": "Delete Me",
        "author": "Test Author",
        "isbn": "111222333",
        "genre": "Test",
        "year": "2021"
    })

    conn = book_app.get_db_connection()
    book = conn.execute(
        "SELECT id FROM books WHERE isbn = ?", ("111222333",)
    ).fetchone()
    conn.close()

    response = client.post(
        f"/delete/{book['id']}", follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Delete Me" not in response.data
