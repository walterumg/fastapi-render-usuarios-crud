# API Usuarios (FastAPI + Postgres)

## Local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:password@localhost:5432/mi_api
uvicorn app.main:app --reload
```
