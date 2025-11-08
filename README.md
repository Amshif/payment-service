# 💳 Payment Service (FastAPI + Poetry + Razorpay)

This is a **Payment Microservice** for an E-Commerce application, built using **FastAPI** and **Poetry (2025)**.  
It integrates with **Razorpay** for payment processing, supports **refunds**, **webhooks**, and **event-based updates**.  
This service is designed to work in a **microservice architecture**, alongside an **Order Service** and a **User Service**.

---

## 🧩 Tech Stack

- **Python 3.11+**
- **FastAPI**
- **Poetry (>=1.8)**
- **PostgreSQL**
- **SQLAlchemy**
- **Razorpay SDK**
- **Uvicorn**
- **Pydantic v2**
- **dotenv** for environment configuration

---

## 📁 Project Structure

```
payment_backend/
│
├── pyproject.toml                 # Poetry dependencies, build info
├── README.md                      # Project documentation
├── Dockerfile                     # Container setup (optional)
├── .env                           # Environment variables
│
└── src/
    └── app/
        ├── main.py                # FastAPI entry point
        │
        ├── core/                  # Core configurations & setup
        │   ├── config.py          # Env vars (API keys, DB URI, etc.)
        │   ├── database.py        # SQLAlchemy SessionLocal & Base
        │   ├── logging_config.py  # Custom logging setup
        │   └── security.py        # (Optional) if you add API keys, auth
        │
        ├── db/
        │   ├── create_tables.sql  # SQL schema (Postgres / any RDBMS)
        │   └── migrations/        # Alembic migrations (optional)
        │
        ├── models/                # SQLAlchemy ORM models
        │   ├── payments.py
        │   ├── refunds.py
        │   ├── webhooks.py
        │   └── audit_logs.py
        │
        ├── schemas/               # Pydantic schemas (v2)
        │   ├── payments.py
        │   ├── refunds.py
        │   ├── webhooks.py
        │   └── common.py
        │
        ├── repositories/          # Data access layer (CRUD operations)
        │   ├── payments_repository.py
        │   ├── refunds_repository.py
        │   ├── webhooks_repository.py
        │   └── base_repository.py  # shared logic for repos (optional)
        │
        ├── services/              # Business logic layer
        │   ├── payments_service.py
        │   ├── refunds_service.py
        │   ├── webhooks_service.py
        │   └── settlements_service.py
        │
        ├── routers/               # FastAPI route definitions
        │   ├── v1/                # Versioned API
        │   │   ├── payments_router.py
        │   │   ├── refunds_router.py
        │   │   ├── webhooks_router.py
        │   │   ├── settlements_router.py
        │   │   └── health_router.py
        │   └── __init__.py
        │
        ├── utils/                 # Helper modules
        │   ├── gateway_client.py  # Razorpay/Stripe wrapper
        │   ├── idempotency.py     # Idempotency-key helper
        │   ├── event_publisher.py # Emits internal payment events
        │   └── common.py          # Misc helpers
        │
        ├── exceptions/            # Centralized exception handlers
        │   ├── http_exceptions.py
        │   └── payment_exceptions.py
        │
        └── tests/                 # Unit and integration tests
            ├── test_payments.py
            ├── test_refunds.py
            ├── test_webhooks.py
            └── conftest.py        # pytest fixtures (e.g. test DB)

```

---

## ⚙️ Prerequisites

Before starting, make sure you have:

- 🐍 [Python 3.13+](https://www.python.org/downloads/)
- 📦 [Poetry (>=1.8)](https://python-poetry.org/docs/)
- 🐘 [PostgreSQL](https://www.postgresql.org/download/)
- 🔑 [Razorpay Developer Account](https://razorpay.com)

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/payment-service.git
cd payment-service
```

---

### 2️⃣ Create and Configure the `.env` File

Inside `src/app/`, create a file named `.env` and add the following:

```bash
# Database
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/payment_db

# Razorpay Credentials
RAZORPAY_KEY_ID=rzp_test_xxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxx

# App Config
APP_ENV=development
APP_PORT=8000
```

---

### 3️⃣ Install Dependencies

Use **Poetry** to install all dependencies and create a virtual environment:

```bash
poetry install
```

Poetry will:
- Create a new isolated virtual environment.
- Install dependencies listed in `pyproject.toml`.

---

### 4️⃣ Verify Python Version

Check which Python version your Poetry environment uses:

```bash
poetry env info
```

If the Python version is not 3.13+, fix it with:

```bash
poetry env use 3.13
poetry install
```

Then confirm:

```bash
poetry run python --version
```

✅ Example Output:
```
Python 3.13
```

---

### 5️⃣ Set Up the Database

Make sure PostgreSQL is running, then create your database:

```bash
createdb payment_db
```

Run your SQL schema to initialize all tables:

```bash
psql -U postgres -d payment_db -f src/app/db/create_tables.sql
```

---

### 6️⃣ Run the Application

#### 🔹 Development Mode (with live reload)
```bash
poetry run uvicorn app.main:app --reload
```

#### 🔹 Production Mode
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Your app will be live at:
👉 http://localhost:8000

---

## 🧭 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **POST** | `/api/v1/payments/create` | Create Razorpay order and internal payment record |
| **GET** | `/api/v1/payments/{id}` | Get payment details by ID |
| **POST** | `/api/v1/refunds/` | Initiate a refund |
| **POST** | `/api/v1/webhooks/razorpay` | Receive Razorpay webhook events |
| **GET** | `/health` | Health check endpoint |

### 📘 API Docs

Once running:
- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧰 Useful Poetry Commands

| Command | Description |
|----------|-------------|
| `poetry install` | Install dependencies |
| `poetry add fastapi` | Add a new dependency |
| `poetry add --group dev pytest` | Add a dev dependency |
| `poetry run uvicorn app.main:app --reload` | Run the app |
| `poetry run pytest` | Run test suite |
| `poetry env info` | View virtual environment details |
| `poetry env use 3.11` | Use a specific Python version |
| `poetry export -f requirements.txt --output requirements.txt --without-hashes` | Export dependencies for non-Poetry users |

---

## 🧪 Testing

Run all tests using:

```bash
poetry run pytest -v
```

To use a test environment, set:
```
APP_ENV=test
```

and configure a separate test database in `.env.test` if needed.

---

## 🐳 Docker (Optional)

To containerize the Payment Service and PostgreSQL together:

1. Create a `docker-compose.yml` file:

```yaml
version: "3.9"

services:
  payment_service:
    build: .
    command: poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    env_file:
      - src/app/.env
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: payment_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  pg_data:
```

2. Run with:
```bash
docker compose up --build
```

Then visit:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📜 License

MIT License © 2025 Amshif

---

## 👨‍💻 Author

**AMSHIF**  
Backend Developer • E-Commerce & Payment Systems  
📧 amshif313@gmail.com 
🔗 [LinkedIn](https://linkedin.com/in/yourprofile)
