import time
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import settings
from app.routes.books import router as books_router
from app.utils.logger import logger

# Initialize FastAPI application with project metadata
app = FastAPI(
    title=settings.app_name,
    description="Professional RESTful API for managing library inventory",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    """
    Custom middleware to capture and log HTTP transaction details,
    including request methods, URLs, latencies, and response statuses.
    """
    start_time = time.perf_counter()
    method = request.method
    path = request.url.path
    
    logger.info(f"Incoming request: {method} {path}")
    
    try:
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"Completed request: {method} {path} | "
            f"Status: {response.status_code} | "
            f"Latency: {process_time:.2f}ms"
        )
        return response
    except Exception as exc:
        process_time = (time.perf_counter() - start_time) * 1000
        logger.error(
            f"Unhandled exception during: {method} {path} | "
            f"Error: {str(exc)} | "
            f"Latency: {process_time:.2f}ms",
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An internal server error occurred."}
        )

from fastapi.encoders import jsonable_encoder

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for Pydantic validation errors to log validation details
    and return standard RFC-compliant JSON response payloads.
    """
    errors = exc.errors()
    sanitized_errors = []
    
    for err in errors:
        sanitized_err = dict(err)
        # Convert any non-serializable Exception objects in ctx (like ValueError) to strings
        if "ctx" in sanitized_err and isinstance(sanitized_err["ctx"], dict):
            sanitized_err["ctx"] = {
                k: str(v) if isinstance(v, Exception) else v
                for k, v in sanitized_err["ctx"].items()
            }
        sanitized_errors.append(sanitized_err)

    logger.warning(
        f"Validation failed for request: {request.method} {request.url.path} | "
        f"Errors: {sanitized_errors}"
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": sanitized_errors,
            "message": "Input validation failed. Please check the requested fields."
        })
    )

@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["Root"],
    summary="API Root Information",
    description="Retrieve base API documentation links and deployment metadata."
)
def read_root():
    return {
        "title": app.title,
        "description": app.description,
        "version": app.version,
        "environment": settings.environment,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "health": "/health",
            "books_v1": "/api/v1/books",
            "books_legacy": "/books"
        }
    }

@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="API Health Status",
    description="Check service health status, current timestamp, and API version."
)
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": app.version
    }

# Register API Routers
# 1. Versioned Route (Self-documented in Swagger UI)
app.include_router(books_router, prefix="/api/v1/books", tags=["Books (v1)"])

# 2. Legacy Route (Hidden from Swagger UI for compatibility but fully active)
app.include_router(books_router, prefix="/books", include_in_schema=False)
