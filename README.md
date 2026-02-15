# 💰 Expenses Tracker API

REST API for personal expense tracking built with FastAPI, PostgreSQL, Redis, and Celery.

## 🚀 Features


- RESTful API for expenses, categories, and users management
- Async database operations with SQLAlchemy
- Redis caching for better performance
- Background tasks with Celery
- Database migrations with Alembic
- Request logging with automatic rotation
- Docker containerization
- GitLab CI/CD pipeline

## 🛠 Tech Stack

- **FastAPI** + **Uvicorn** - Web framework & ASGI server
- **PostgreSQL** + **SQLAlchemy** - Database & ORM
- **Redis** - Caching & message broker
- **Celery** - Background task processing
- **Docker** - Containerization
- **Alembic** - Database migrations
- **pytest** - Testing framework
- **Ruff** - Linting & formatting

## 📁 Project Structure

```
src/
├── api/routers/        # API endpoints (users, expenses, categories)
├── cache/              # Redis caching layer
├── config/             # Settings & logging configuration
├── db/                 # Database models
├── migrations/         # Alembic migrations
├── schemas/            # Pydantic schemas
├── services/           # Business logic
├── tasks/              # Celery tasks
└── main.py             # App entry point
```

## 🚦 Quick Start

### Prerequisites
- Docker & Docker Compose

### 1. Clone & Configure

```bash
git clone https://github.com/teohchik/fast_api_learning
cd fast_api_learning
```

Copy example environment files and configure:
```bash
cp .env-example .env
cp .env-test-example .env-test
```

Edit `.env` with your actual values:
```env
MODE=LOCAL
API_KEY=your_secret_api_key_here

DB_NAME=expenses
DB_HOST=expenses_db
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password

REDIS_HOST=expenses_cache
REDIS_PORT=6379
```

### 2. Setup Infrastructure (One-time setup)

First, create Docker network:
```bash
docker network create myNetwork
```

Start PostgreSQL database:
```bash
docker run --name expenses_db \
  -p 6432:5432 \
  -e POSTGRES_USER=your_db_user \
  -e POSTGRES_PASSWORD=your_db_password \
  -e POSTGRES_DB=expenses \
  --network=myNetwork \
  --volume pg-expenses-data:/var/lib/postgresql/data \
  -d postgres:17
```

Start Redis cache:
```bash
docker run --name expenses_cache \
  -p 7379:6379 \
  --network=myNetwork \
  -d redis:8.4
```

Start Nginx reverse proxy:
```bash
docker run --name expenses_nginx \
  --volume ./nginx.conf:/etc/nginx/nginx.conf \
  --network=myNetwork \
  -p 80:80 \
  -d nginx
```

> **Note:** These infrastructure containers need to be started only once. They will persist across restarts.

### 3. Run Application

```bash
docker compose up —build -d
```

This starts:
- FastAPI application
- Celery worker
- Celery beat scheduler

### 4. Access API
- API Documentation: http://localhost/docs
- Alternative docs: http://localhost/redoc

### Stopping Application

```bash
# Stop only application containers
docker compose down

# Keep infrastructure running (DB, Redis, Nginx)
```

## 🧪 Testing

```bash
# Run all tests
pytest -v


```

## 📊 Logging

Logs are saved to `logs/app.log` with automatic rotation (10MB max, 3 backups).

Format:
```
2026-02-10 20:53:15,589 - root - INFO - Successfully connected to Redis
```

## 🎯 API Endpoints

### Users
- `POST /users` - Create user
- `GET /users/{id}` - Get user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Expenses
- `POST /expenses` - Create expense
- `GET /expenses` - List expenses
- `GET /expenses/{id}` - Get expense
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense

### Categories
- `POST /categories` - Create category
- `GET /categories` - List categories
- `GET /categories/{id}` - Get category
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

## 🔄 CI/CD Pipeline

GitLab CI stages:
1. **Build** - Docker image
2. **Lint/Format** - Ruff checks
3. **Migrations** - Database updates
4. **Tests** - Full test suite
5. **Deploy** - Automatic deployment

## 🛠 Development

### Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
python src/main.py
```

### Code Quality

```bash
# Linting
ruff check

# Format code
ruff format
```

## 📄 License

Personal learning project and portfolio piece.

## 👤 Author

- GitHub: [@teohchik](https://github.com/teohchik)
- LinkedIn: [linkedin.com/in/teosha](https://linkedin.com/in/teosha)

---

⭐ Star this repo if you find it useful!
