from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class BookBase(BaseModel):
    """
    Base attributes shared by book schemas.
    """
    title: str = Field(..., min_length=2, description="Title of the book (minimum 2 characters)")
    author: str = Field(..., description="Author of the book (cannot be empty)")
    publication_year: int = Field(..., gt=0, description="Publication year (must be a positive integer)")
    genre: str = Field(..., description="Genre of the book (cannot be empty)")

    @field_validator("title", "author", "genre")
    @classmethod
    def validate_non_empty_strings(cls, v: str, info) -> str:
        """
        Custom validator to prevent whitespace-only or empty strings.
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError(f"Field '{info.field_name}' cannot be empty or only whitespace.")
        if info.field_name == "title" and len(stripped) < 2:
            raise ValueError("Title must contain at least 2 non-whitespace characters.")
        return stripped

    @field_validator("publication_year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        """
        Ensure the publication year is not in the unrealistic future.
        """
        current_year = datetime.now().year
        limit_year = current_year + 2
        if v > limit_year:
            raise ValueError(f"Publication year cannot be greater than {limit_year}.")
        return v

class BookCreate(BookBase):
    """
    Schema for creating a new book.
    """
    pass

class BookUpdate(BaseModel):
    """
    Schema for updating book details. All fields are optional.
    """
    title: str | None = Field(None, min_length=2, description="Title of the book")
    author: str | None = Field(None, description="Author of the book")
    publication_year: int | None = Field(None, gt=0, description="Publication year")
    genre: str | None = Field(None, description="Genre of the book")
    available: bool | None = Field(None, description="Availability status of the book")

    @field_validator("title", "author", "genre")
    @classmethod
    def validate_non_empty_strings(cls, v: str | None, info) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError(f"Field '{info.field_name}' cannot be empty or only whitespace.")
        if info.field_name == "title" and len(stripped) < 2:
            raise ValueError("Title must contain at least 2 non-whitespace characters.")
        return stripped

    @field_validator("publication_year")
    @classmethod
    def validate_year(cls, v: int | None) -> int | None:
        if v is None:
            return v
        current_year = datetime.now().year
        limit_year = current_year + 2
        if v > limit_year:
            raise ValueError(f"Publication year cannot be greater than {limit_year}.")
        return v

class Book(BookBase):
    """
    Schema representing a book fully persisted in the database.
    """
    id: int = Field(..., description="Unique database identifier")
    available: bool = Field(True, description="Indicates if the book is currently available in the library")
