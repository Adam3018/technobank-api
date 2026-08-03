# SETUP instructions

This document explains how to create and use a single virtual environment located in the `technobank-api` folder and how to start the application.

## Prerequisites

- Python 3.8+ installed. Download: https://www.python.org/downloads/
- When installing on Windows, check "Add Python to PATH".

## Windows (recommended)

1. Open PowerShell or Command Prompt and change into the project API folder:

```powershell
cd D:\TechnoBank2.0\technobank-api
```

2. Create the virtual environment (one time):

```powershell
python -m venv venv
```

3. Activate the virtual environment:

- PowerShell (use this if you prefer PS):

```powershell
.\venv\Scripts\Activate.ps1
# If you see an execution policy error, run once as admin:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- Command Prompt (cmd.exe):

```cmd
venv\Scripts\activate.bat
```

4. Install dependencies into the `venv`:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Start the application (recommended to use the venv python to avoid PATH issues):

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
