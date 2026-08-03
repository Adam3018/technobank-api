# FastAPI CRUD Startup - Development Guidelines

## Project Overview
A production-ready FastAPI CRUD application with SQLAlchemy ORM and Pydantic validation.

## Development Standards
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and returns
- Implement proper error handling with HTTP exceptions
- Use Pydantic models for request/response validation
- Maintain separation of concerns: routes, schemas, CRUD, models

## Running the Application
- Development: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Production: Use Gunicorn with Uvicorn workers

## Testing
- Run tests with pytest: `pytest`
- Test coverage should be maintained above 80%

## Database
- SQLite for development (auto-created)
- SQLAlchemy ORM for database operations
- Alembic for migrations (if needed)

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
