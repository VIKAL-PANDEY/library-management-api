from app.database.data import db
from app.models.book import Book, BookCreate, BookUpdate
from app.utils.logger import logger

class BookService:
    """
    Service layer containing business logic rules for managing Books.
    """
    @staticmethod
    def get_all_books(genre: str | None = None, available: bool | None = None) -> list[Book]:
        """
        Retrieves all books from database and applies optional filters for genre and availability.
        """
        logger.info(f"Service: Retrieving books with filters - genre={genre}, available={available}")
        books = db.get_all()

        # Filter by genre (case-insensitive)
        if genre is not None:
            clean_genre = genre.strip().lower()
            books = [b for b in books if b.genre.strip().lower() == clean_genre]

        # Filter by availability
        if available is not None:
            books = [b for b in books if b.available == available]

        return books

    @staticmethod
    def get_book_by_id(book_id: int) -> Book | None:
        """
        Retrieves a single book by ID.
        """
        logger.info(f"Service: Retrieving book details for ID {book_id}")
        return db.get_by_id(book_id)

    @staticmethod
    def create_book(book_data: BookCreate) -> Book:
        """
        Creates a new book.
        """
        logger.info(f"Service: Creating book: '{book_data.title}' by {book_data.author}")
        return db.create(book_data)

    @staticmethod
    def update_book(book_id: int, book_data: BookUpdate) -> Book | None:
        """
        Updates book details for a given book ID.
        """
        logger.info(f"Service: Updating book ID {book_id}")
        return db.update(book_id, book_data)

    @staticmethod
    def delete_book(book_id: int) -> bool:
        """
        Deletes a book by its ID.
        """
        logger.info(f"Service: Deleting book ID {book_id}")
        return db.delete(book_id)
