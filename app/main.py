"""
FastAPI application entry point
"""

import os
import sys
import webbrowser
from threading import Timer

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import Base, engine
from app.api.routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="FastAPI CRUD API",
    description="A production-ready CRUD API built with FastAPI",
    version="1.0.0"
)

# Uploads directory for floor plans
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(router)



@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# --- SERVE REACT FRONTEND ---

def get_ui_path():
    """Locate assets whether running as source Python or PyInstaller executable."""
    if getattr(sys, 'frozen', False):
        # PyInstaller extracts bundled files to _MEIPASS at runtime
        return os.path.join(sys._MEIPASS, "technobank-ui-dist")
    # Development path relative to main.py
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../technobank-ui/dist"))


ui_path = get_ui_path()

if os.path.exists(ui_path):
    assets_path = os.path.join(ui_path, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_react_app(full_path: str):
        """Catch-all route to serve index.html for React Router / client-side routing."""
        # Allow access to direct static files if placed in public directory
        requested_file = os.path.join(ui_path, full_path)
        if full_path != "" and os.path.exists(requested_file) and os.path.isfile(requested_file):
            return FileResponse(requested_file)
        return FileResponse(os.path.join(ui_path, "index.html"))


def open_browser():
    """Automatically launches the user's default browser on startup."""
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    import sys
    import uvicorn

    # Fix for PyInstaller --windowed mode where sys.stdout / sys.stderr are None
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

    # Start browser timer
    Timer(1.2, open_browser).start()

    # Pass use_colors=False to prevent uvicorn logging crashes
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000, 
        use_colors=False, 
        log_config=None  # Disables default uvicorn logging formatter
    )