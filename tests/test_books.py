import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.data import db
from app.models.book import BookCreate

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    """
    Fixture that runs automatically before each test to clear the database
    and re-seed initial data, ensuring complete test case isolation.
    """
    db._books.clear()
    db._current_id = 0
    db._seed_data()

def test_root_endpoint():
    """Test retrieving API metadata from the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Library Management API"
    assert "docs_url" in data
    assert "endpoints" in data

def test_health_check():
    """Test checking API health status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data

def test_get_all_books():
    """Test fetching all books from the versioned endpoint."""
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["title"] == "1984"

def test_get_all_books_legacy():
    """Test fetching all books from the legacy route (backward compatibility)."""
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

def test_get_books_filtering():
    """Test books query parameters filtering by genre and availability."""
    # Filter by genre
    response = client.get("/api/v1/books?genre=Classic")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "The Great Gatsby"

    # Filter by availability
    response = client.get("/api/v1/books?available=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

    # Filter with non-matching genre
    response = client.get("/api/v1/books?genre=NonExistentGenre")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_get_single_book():
    """Test retrieving a single book details by ID."""
    response = client.get("/api/v1/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"

def test_get_single_book_not_found():
    """Test retrieving a non-existent book ID yields 404."""
    response = client.get("/api/v1/books/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_create_book_success():
    """Test successful book creation."""
    payload = {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "publication_year": 1932,
        "genre": "Dystopian"
    }
    response = client.post("/api/v1/books", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 6
    assert data["title"] == "Brave New World"
    assert data["available"] is True

def test_create_book_validation_fails():
    """Test that input validation failures yield HTTP 422."""
    # Title too short (< 2 characters)
    payload_short_title = {
        "title": "A",
        "author": "Aldous Huxley",
        "publication_year": 1932,
        "genre": "Dystopian"
    }
    response = client.post("/api/v1/books", json=payload_short_title)
    assert response.status_code == 422

    # Negative publication year
    payload_neg_year = {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "publication_year": -10,
        "genre": "Dystopian"
    }
    response = client.post("/api/v1/books", json=payload_neg_year)
    assert response.status_code == 422

    # Empty/whitespace author name
    payload_empty_author = {
        "title": "Brave New World",
        "author": "   ",
        "publication_year": 1932,
        "genre": "Dystopian"
    }
    response = client.post("/api/v1/books", json=payload_empty_author)
    assert response.status_code == 422

    # Unrealistic future publication year
    payload_future_year = {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "publication_year": 2100,
        "genre": "Dystopian"
    }
    response = client.post("/api/v1/books", json=payload_future_year)
    assert response.status_code == 422

def test_update_book_success():
    """Test updating details on an existing book."""
    payload = {
        "title": "1984 - Modern Edition",
        "available": False
    }
    response = client.put("/api/v1/books/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "1984 - Modern Edition"
    assert data["available"] is False
    assert data["author"] == "George Orwell"  # Preserved original fields

def test_update_book_not_found():
    """Test updating a non-existent book yields 404."""
    payload = {"title": "New Title"}
    response = client.put("/api/v1/books/999", json=payload)
    assert response.status_code == 404

def test_delete_book_success():
    """Test successfully deleting a book record."""
    response = client.delete("/api/v1/books/1")
    assert response.status_code == 200
    data = response.json()
    assert "successfully deleted" in data["message"].lower()

    # Re-retrieve should fail with 404
    get_response = client.get("/api/v1/books/1")
    assert get_response.status_code == 404

def test_delete_book_not_found():
    """Test deleting a non-existent book yields 404."""
    response = client.delete("/api/v1/books/999")
    assert response.status_code == 404
