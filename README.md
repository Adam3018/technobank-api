# TechnoBank API

FastAPI CRUD backend for TechnoBank.

## Installation

**Windows:**
```bash
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

## Running

Activate venv and start server:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## Database

SQLite (`test.db`) by default. Update `SQLALCHEMY_DATABASE_URL` in `app/database.py` to use a different database.

## Development

- Models: `app/models/`
- Schemas: `app/schemas/`
- CRUD: `app/crud/`
- Routes: `app/api/routes/`
```

## Production Deployment

For production, use Gunicorn with Uvicorn workers:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

## Environment Variables

Create a `.env` file in the root directory for configuration:
```
DATABASE_URL=sqlite:///./test.db
DEBUG=False
```

## Dependencies

- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and parsing
- **Python-dotenv** - Environment variable management

## License

MIT License - Feel free to use this project for learning and development.

## Contributing

Contributions are welcome! Please follow PEP 8 style guidelines and maintain test coverage.
