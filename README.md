Internship TASK 1

NAME:- VIKAL PANDEY 
COMPANY:- CODTECH IT SOLOUTIONS 
INTERN ID :- CTIS8713 
MENTOR:- Neela Santhosh 
Duration:- 6 Weeks 
Domain:- Software Development

#OUTPUT#

https://github.com/VIKAL-PANDEY/library-management-api/issues/1#issue-4603840468



# Library Management API

[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0%20%2B-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-quality RESTful API built with **FastAPI** for managing a library inventory. Designed using professional clean architecture guidelines, a thread-safe repository service-layer pattern, rigorous validation schemas with Pydantic, and automated request logging.

---

## 1. Project Overview
This repository implements a fully featured RESTful API designed to manage books in a library inventory. It is built as a portfolio project suitable for software engineering internship showcases, emphasizing:
- **Clean Architecture**: Strong decoupling of routes, services, data validation, and core configuration.
- **Service Layer Pattern**: Business logic resides strictly in services, maintaining clean endpoints.
- **Thread-Safety**: Handled in-memory storage utilizing standard Python thread locks to protect concurrent resource updates.
- **Comprehensive API Documentation**: Fully supports automatic Swagger UI and ReDoc pages.
- **Robust Exception Handling**: Custom middlewares and filters converting validation exceptions and server errors to RFC-compliant standardized JSON responses.

---

## 2. Features
- **Book Inventory Management (CRUD)**: Create, Read (all or singular), Update, and Delete books.
- **Advanced Filtering**: Search books by `genre` and availability (`available = true/false`).
- **Input Validation**: Strict schema checks (e.g. minimum character lengths, preventing whitespace-only strings, range checks for publication years).
- **Request Tracing Middleware**: Automated structured logs recording HTTP verbs, resource routes, response statuses, and execution latencies.
- **Backward Compatibility**: Fully supports unversioned legacy routes (e.g. `/books`) and redirects to versioned (`/api/v1/books`) structures without breaking API usage.
- **Health Diagnostics**: Active monitoring checks `/health`.

---

## 3. Tech Stack
- **Web Framework**: FastAPI (0.111.0+)
- **Validation & Serialization**: Pydantic (2.7.0+)
- **Server Runner**: Uvicorn (0.30.0+)
- **Setting Manager**: Pydantic Settings (2.2.0+)
- **Testing Framework**: Pytest (9.0.0+) & HTTPX (for async requests testing)
- **Language**: Python 3.12+ (tested up to Python 3.14)

---

## 4. Folder Structure
```text
library-management-api/
├── app/
│   ├── main.py                 # FastAPI application initializer & configuration
│   ├── config.py               # Pydantic Settings schema loading from .env
│   ├── database/
│   │   └── data.py             # Thread-safe in-memory database store & seed data
│   ├── models/
│   │   └── book.py             # Pydantic schema validation models
│   ├── routes/
│   │   └── books.py            # API request routes mapping CRUD operations
│   ├── services/
│   │   └── book_service.py     # Decoupled service layer handling business logic
│   └── utils/
│       └── logger.py           # Structured logger configuration
├── tests/
│   └── test_books.py           # Integration and unit tests using pytest & TestClient
├── requirements.txt            # Dependency file pinning packages
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── .gitignore                  # Git tracking rules
├── .env                        # Active local configuration variables
└── .env.example                # Template configuration variables
```

---

## 5. Installation Guide
Ensure you have Python 3.12+ installed. Run the following commands:

### Create Virtual Environment
```bash
# Clone the repository and navigate inside
cd library-management-api

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (Command Prompt)
venv\Scripts\activate.bat
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# On macOS/Linux
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 6. Running Locally

### 1. Setup Environment
Initialize the environment configuration file:
```bash
cp .env.example .env
```

### 2. Start Server
Run the local development server:
```bash
uvicorn app.main:app --reload
```
By default, the server spins up at: `http://127.0.0.1:8000`

### 3. Run Automated Tests
Verify that all API actions, routing, and validations are working correctly:
```bash
python -m pytest tests/ -v
```

---

## 7. API Documentation URLs
FastAPI automatically registers and serves interactive, standard documentation:
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc Schema Explorer**: `http://127.0.0.1:8000/redoc`

---

## 8. Endpoint Table

| Verb | Endpoint | Description | Query Parameters | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/` | Fetch basic API information & docs links | None | `200` |
| **GET** | `/health` | Fetch application health status | None | `200` |
| **GET** | `/api/v1/books` | Retrieve book inventory | `genre` (str), `available` (bool) | `200` |
| **GET** | `/api/v1/books/{id}`| Fetch a singular book by its ID | None | `200`, `404` |
| **POST**| `/api/v1/books` | Create/Insert a new book | None | `201`, `422` |
| **PUT** | `/api/v1/books/{id}`| Update fields on an existing book | None | `200`, `404`, `422` |
| **DELETE**| `/api/v1/books/{id}`| Delete a book from inventory | None | `200`, `404` |

> [!NOTE]
> All legacy endpoints (e.g. `/books`, `/books/{id}`) are fully backward-compatible and mirror the versioned endpoints. They are hidden from the Swagger UI documentation to avoid clutter.

---

## 9. Example Requests & Responses

### 1. Create a Book
* **Request**: `POST /api/v1/books`
```json
{
  "title": "Brave New World",
  "author": "Aldous Huxley",
  "publication_year": 1932,
  "genre": "Dystopian"
}
```
* **Response**: `201 Created`
```json
{
  "id": 6,
  "title": "Brave New World",
  "author": "Aldous Huxley",
  "publication_year": 1932,
  "genre": "Dystopian",
  "available": true
}
```

### 2. Retrieve Books (With Filtering)
* **Request**: `GET /api/v1/books?genre=Classic`
* **Response**: `200 OK`
```json
[
  {
    "id": 3,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "publication_year": 1925,
    "genre": "Classic",
    "available": true
  }
]
```

### 3. Handle Validation Error
* **Request**: `POST /api/v1/books`
```json
{
  "title": "A",
  "author": " ",
  "publication_year": -5,
  "genre": "Sci-Fi"
}
```
* **Response**: `422 Unprocessable Content`
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 2 characters",
      "input": "A",
      "ctx": {"min_length": 2}
    },
    {
      "type": "value_error",
      "loc": ["body", "author"],
      "msg": "Value error, Field 'author' cannot be empty or only whitespace.",
      "input": "   ",
      "ctx": {"error": "Field 'author' cannot be empty or only whitespace."}
    },
    {
      "type": "greater_than",
      "loc": ["body", "publication_year"],
      "msg": "Input should be greater than 0",
      "input": -5,
      "ctx": {"gt": 0}
    }
  ],
  "message": "Input validation failed. Please check the requested fields."
}
```

---

## 10. Future Improvements
1. **Persistent Database Integration**: Replace the in-memory database store with an ORM like **SQLAlchemy** or **SQLModel** linking to a relational database engine (PostgreSQL/SQLite).
2. **Authentication & Authorization**: Add secure endpoint guards via **OAuth2 with JWT tokens** to secure update and delete operations.
3. **Pagination**: Implement pagination query params (`limit`, `offset`) on book collection list views.
4. **CI/CD Pipeline**: Define GitHub Actions workflows to auto-run pytest suites and format checks on pull requests.

---

## 11. License
Distributed under the **MIT License**. See `LICENSE` for details.
