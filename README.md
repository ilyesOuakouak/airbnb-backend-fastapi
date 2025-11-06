# 🏡 Airbnb Backend — FastAPI Clone

A **scalable backend API** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** — inspired by Airbnb architecture.  
Designed to follow modern backend engineering practices (async I/O, modular design, Docker, CI/CD, monitoring).

---

## 🚀 Tech Stack

| Layer | Technology                               |
|-------|------------------------------------------|
| Backend Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM | SQLAlchemy + Alembic                     |
| Database | PostgreSQL                               |
| Auth | JWT (coming soon)                        |
| Caching / Queue | Redis + Celery (Phase 2)                 |
| Deployment | Docker + Scaleway or AWS                 |
| Monitoring | Prometheus + Grafana (Phase 3)           |

---

## 🧩 Project Phases

**Phase 1 — Core Backend (Current)**  
- FastAPI setup + PostgreSQL  
- Users module (`/users/register`, `/users/list`)  
- Pydantic validation + password hashing  
- Alembic migrations

**Next:**  
- `/login` endpoint with JWT  
- `/me` protected route  
- Docker integration

---

## 🧱 Project Structure

app/
 ├─ __init__.py
 ├─ main.py
 ├─ api/
 │   ├─ __init__.py
 │   └─ user.py
 ├─ core/
 │   ├─ __init__.py
 │   ├─ config.py
 │   └─ database.py
 ├─ models/
 │   ├─ __init__.py
 │   └─ user.py
 ├─ schemas/
 │   ├─ __init__.py
 │   └─ user.py
 └─ services/
     ├─ __init__.py
     └─ user_service.py

## ⚙️ Setup

```bash
# 1️⃣ Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run database migrations
alembic upgrade head

# 4️⃣ Start FastAPI server
uvicorn app.main:app --reload


