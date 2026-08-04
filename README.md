## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

### Interactive API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

The application uses SQLite by default. The database file (`test.db`) is automatically created on first run.

To use a different database:
1. Update `SQLALCHEMY_DATABASE_URL` in `app/database.py`
2. Install the appropriate database driver for your chosen database

## Development

### Adding New Models
1. Create a model class in `app/models/`
2. Create schemas in `app/schemas/`
3. Create CRUD operations in `app/crud/`
4. Create routes in `app/api/routes/`
5. Include the router in `app/main.py`

### Testing
Run tests with pytest:
```bash
pytest
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
