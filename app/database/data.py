import threading
from app.models.book import Book, BookCreate, BookUpdate

class InMemoryBookDatabase:
    """
    A thread-safe in-memory database simulating standard database CRUD operations.
    Protected by threading.Lock to avoid race conditions.
    """
    def __init__(self):
        self._books: dict[int, Book] = {}
        self._current_id = 0
        self._lock = threading.Lock()
        self._seed_data()

    def _seed_data(self) -> None:
        """
        Seeds the database with classic sample books for testing and visualization.
        """
        seed_books = [
            BookCreate(title="1984", author="George Orwell", publication_year=1949, genre="Dystopian"),
            BookCreate(title="To Kill a Mockingbird", author="Harper Lee", publication_year=1960, genre="Fiction"),
            BookCreate(title="The Great Gatsby", author="F. Scott Fitzgerald", publication_year=1925, genre="Classic"),
            BookCreate(title="The Hobbit", author="J.R.R. Tolkien", publication_year=1937, genre="Fantasy"),
            BookCreate(title="Fahrenheit 451", author="Ray Bradbury", publication_year=1953, genre="Sci-Fi"),
        ]
        for book_data in seed_books:
            self.create(book_data)

    def create(self, book_data: BookCreate) -> Book:
        """
        Inserts a new book record.
        """
        with self._lock:
            self._current_id += 1
            new_book = Book(
                id=self._current_id,
                title=book_data.title,
                author=book_data.author,
                publication_year=book_data.publication_year,
                genre=book_data.genre,
                available=True
            )
            self._books[self._current_id] = new_book
            return new_book

    def get_all(self) -> list[Book]:
        """
        Returns a copy of all book records.
        """
        with self._lock:
            return list(self._books.values())

    def get_by_id(self, book_id: int) -> Book | None:
        """
        Returns a single book by ID or None.
        """
        with self._lock:
            return self._books.get(book_id)

    def update(self, book_id: int, book_data: BookUpdate) -> Book | None:
        """
        Updates fields on an existing book record. Only updates provided fields.
        """
        with self._lock:
            if book_id not in self._books:
                return None
            
            existing_book = self._books[book_id]
            # Get updated fields as a dictionary, ignoring fields that weren't sent
            update_fields = book_data.model_dump(exclude_unset=True)
            
            # Merge existing attributes with changes
            merged_data = existing_book.model_dump()
            merged_data.update(update_fields)
            
            # Save and return updated instance
            updated_book = Book(**merged_data)
            self._books[book_id] = updated_book
            return updated_book

    def delete(self, book_id: int) -> bool:
        """
        Deletes a book record by its ID. Returns True if deleted, False otherwise.
        """
        with self._lock:
            if book_id in self._books:
                del self._books[book_id]
                return True
            return False

# Global database singleton
db = InMemoryBookDatabase()
