# Setup

## Requirements
- Python 3.8+ installed

## Windows
```bash
setup.bat
```

## Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
```

## Run
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

View API docs: http://localhost:8000/docs
# or explicitly: .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## macOS / Linux

1. Open Terminal and change into the API folder:

```bash
cd /path/to/TechnoBank2.0/technobank-api
```

2. Create and activate the venv:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies and start the app:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Notes & Troubleshooting

- Use only the `venv` folder under `technobank-api`; delete other envs in the workspace root to avoid confusion.
- If you see `ModuleNotFoundError: No module named 'app'`, ensure your current working directory is `D:\TechnoBank2.0\technobank-api` when running uvicorn.
- If `Activate.ps1` fails in PowerShell due to execution policy, run as admin once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- To run uvicorn using the venv's Python explicitly (works even if activation doesn't set PATH):

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Access the running app

- API docs (Swagger): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health
- Root: http://localhost:8000/

## Next steps

- Review [README.md](README.md) for API details.
- If you want, I can update `setup.bat`/`setup.sh` to create the venv inside `technobank-api` automatically.
