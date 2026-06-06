from fastapi import APIRouter, HTTPException, status, Query
from app.models.book import Book, BookCreate, BookUpdate
from app.services.book_service import BookService

router = APIRouter()

@router.get(
    "/",
    response_model=list[Book],
    status_code=status.HTTP_200_OK,
    summary="Get all books",
    description="Retrieve all books from the library inventory. Optional filters can be applied for genre and availability."
)
def get_books(
    genre: str | None = Query(None, description="Filter books by genre"),
    available: bool | None = Query(None, description="Filter books by availability (true/false)")
):
    return BookService.get_all_books(genre=genre, available=available)

@router.get(
    "/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    summary="Get a book by ID",
    description="Retrieve the details of a specific book by its unique ID."
)
def get_book(book_id: int):
    book = BookService.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found."
        )
    return book

@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Add a new book to the library inventory. Fields are validated to meet criteria."
)
def create_book(book_data: BookCreate):
    return BookService.create_book(book_data)

@router.put(
    "/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    summary="Update a book by ID",
    description="Update the details of an existing book. Only the fields provided in the body will be updated."
)
def update_book(book_id: int, book_data: BookUpdate):
    updated_book = BookService.update_book(book_id, book_data)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found."
        )
    return updated_book

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a book by ID",
    description="Permanently delete a book from the library inventory by its unique ID."
)
def delete_book(book_id: int):
    deleted = BookService.delete_book(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_444_NOT_FOUND if False else status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found."
        )
    return {"message": f"Book with ID {book_id} has been successfully deleted."}
