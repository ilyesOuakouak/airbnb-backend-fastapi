# 🏡 Airbnb Backend — FastAPI Clone

A **scalable backend API** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** — inspired by Airbnb architecture.  
Designed to follow modern backend engineering practices (async I/O, modular design, Docker, CI/CD, monitoring).

---

## 🚀 Tech Stack

| Layer | Technology                             |
|-------|----------------------------------------|
| Backend Framework | [FastAPI](https://fastapi.tiangolo.com/) (sync + async)|
| ORM | SQLAlchemy + Alembic                   |
| Main Database | PostgreSQL                             |
| Auth | JWT                     |
| Caching / Queue | Redis + Celery          |
| Inter-service Communication | HTTPX (async)          |
| Resilience | Tenacity (Retry) + Custom Circuit Breaker          |
| Microservices | Reservation Service (first extracted service)         |
| Deployment | Docker + Scaleway/AWS (coming)         |
| Monitoring | Prometheus + Grafana (Phase 3)         |


## 🏗️ Project Structure

```
app/
 ├── main.py
 ├── api/
 │    ├── user.py
 │    ├── listing.py
 │    ├── availability.py
 │    └── reservation.py      ← calls reservation microservice
 ├── core/
 │    ├── config.py
 │    ├── auth.py
 │    ├── database.py
 │    ├── redis_client.py
 │    └── circuit_breaker.py  ← custom circuit breaker
 ├── services/
 │    ├── reservation_client.py    ← retry + httpx logic here
 │    ├── user_service.py
 │    └── availability_service.py
 ├── models/
 ├── schemas/
 └── tests/

reservation_service/
 ├── app/
 │    ├── main.py
 │    ├── api/
 │    │    └── reservation.py
 │    ├── core/
 │    │    ├── config.py
 │    │    └── database.py
 │    ├── models/
 │    │    └── reservation.py
 │    ├── schemas/
 │    │    └── reservation.py
 │    └── ...
 ├── alembic/
 └── requirements.txt 
 ```

## Main API Responsibilities

✅ Authentication (JWT) \
✅ Listing CRUD \
✅ Availability + pricing \
✅ Orchestrates reservations \
✅ Sends validated data to microservices \
✅ Uses Circuit Breaker + Retry to survive failures

## Reservation Microservice Responsibilities

✅ Owns reservation_db \
✅ Stores reservations \
✅ No knowledge of users or listings (service isolation principle)

# 🚀 Roadmap
## Phase 1 (Done)

✅ Users Module \
✅ Listings \
✅ Availability \
✅ Redis Cache \
✅ Async SQLAlchemy \

## Phase 2 (Next) — Distributed System

✅ Reservation Microservice \
✅ Retry Strategy \
✅ Circuit Breaker
-[x] Extract User Microservice \
-[x] Extract Listing Microservice \
-[x] API Gateway \
-[x] Global error handler \
-[x] Rate limiting \
-[x] Distributed Tracing (Jaeger) \

## Phase 3 — DevOps

-[x] Docker & Docker Compose
-[x] Reverse Proxy (Traefik or Nginx)
-[x] CI/CD
-[x] Observability (Prometheus + Grafana)

# ⚡ Reliability Features
## 1 - Retry Strategy (Tenacity)
Used when main API calls the Reservation microservice \

    ✅ 3 retries \
    ✅ Exponential backoff (100ms → 200ms → 400ms) \
    ✅ 2s timeout \

This handles transient failures gracefully.

## 2 - Circuit Breaker

Protects the MAIN API from a failing microservice.\
States:

    ✅ CLOSED → Everything OK
    ✅ OPEN → Too many failures → stop sending requests
    ✅ HALF-OPEN → Test if service recovered

Prevents cascading failures across microservices.

## 3 - Redis Caching
Used for:

    ✅ Availability lookups
    ✅ Future caching features
    ✅ Reducing DB load

# ⚙️ Setup Instructions
## 1. Main API Setup

 ``` 
cd app/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

 ```
## 2 - Reservation Microservice Setup

 ``` 

cd reservation_service/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8001

 ``` 




## 👨‍💻 Author
### OUAKOUAK ILYES
Software Engineer | Backend Developer \
[GitHub Profile](https://github.com/ilyesouakouak)


