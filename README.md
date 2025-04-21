# URL Shortener Service

A robust and scalable URL shortening service built with FastAPI, SQLAlchemy, Redis, and Celery. This application provides user authentication, URL shortening, rate limiting, and administrative functionalities, with a focus on performance and security.

## 📚 Table of Contents
- Features
- Technologies
- Project Structure
- Setup Instructions
- API Endpoints
- Running the Application
- Contributing
- License

## 🚀 Features
- **User Authentication**: Secure signup and login with JWT-based authentication.
- **URL Shortening**: Generate unique short URLs with customizable expiration times.
- **Rate Limiting**: Prevent abuse using slowapi with Redis-backed rate limiting.
- **Redis Caching**: Cache frequently accessed URLs for improved performance.
- **Admin Panel**: Manage users and view logs (admin-only access).
- **Background Tasks**: Automatically delete expired URLs using Celery and Redis.
- **Database Integration**: Store user and URL data using SQLAlchemy with SQLite/PostgreSQL support.
- **Logging**: Track admin activities such as user deletion and role changes.

## 🧰 Technologies
- Backend: FastAPI, Python 3.8+
- Database: SQLAlchemy (SQLite/PostgreSQL)
- Caching: Redis
- Task Queue: Celery with Redis as broker and backend
- Authentication: JWT (PyJWT), Passlib (bcrypt)
- Rate Limiting: SlowAPI
- HTTP Client: httpx
- Scheduling: Celery Beat
- Dependencies: Managed via requirements.txt

## 📁 Project Structure
```
url-shortener/
├── main.py                # FastAPI application entry point
├── database.py            # Database configuration and session management
├── modle.py               # SQLAlchemy models
├── auth.py                # Authentication endpoints (signup, login)
├── crud.py                # URL management endpoints (create, update, delete)
├── admin.py               # Admin endpoints (user management, logs)
├── code.py                # Short URL generation logic
├── rate_limitter.py       # Rate limiting configuration
├── redis_client.py        # Redis connection management (commented out)
├── tasks.py               # Celery task for deleting expired URLs
├── worker.py              # Celery worker configuration
├── celeryconfig.py        # Celery Beat scheduling configuration
├── rough.py               # Utility script for testing datetime
```

## 🛠️ Setup Instructions

### 1. Clone the Repository
```
git clone <repository-url>
cd url-shortener
```

### 2. Install Dependencies
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Redis
Install Redis on your system. On Ubuntu:
```
sudo apt install redis-server
```
Make sure Redis is running on `localhost:6379`.

### 4. Database Configuration
Default (SQLite):
```
URL = "sqlite:///./url.db"
```
PostgreSQL:
```
URL = "postgresql://username:password@localhost:5432/ShortUrl"
```

### 5. Environment Setup
Ensure all dependencies are installed. Your `requirements.txt` should include:
```
fastapi
sqlalchemy
redis
celery
slowapi
httpx
pyjwt
passlib[bcrypt]
requests
python-jose
uvicorn
```

### 6. Initialize the Database
Run the app once to create the database tables:
```
python main.py
```

## 🔗 API Endpoints

### Authentication (/auth)
- `POST /signup`: Create a new user account.
- `POST /token`: Generate JWT token for login.

### URL Management (/url)
- `POST /Make_Short_Url/`: Create a short URL (requires authentication).
- `GET /Get_Short`: Retrieve short URLs (requires authentication).
- `PUT /Update_url/`: Update a long URL for a given short URL.
- `DELETE /Delete_Url/`: Delete a short URL.

### General (/)
- `GET /test`: Test database connectivity (rate-limited).
- `GET /shorten/`: Retrieve long URL from short URL (rate-limited).

### Admin (/admin)
- `PUT /Be_Admin/`: Grant admin role (requires admin code).
- `GET /All_USer`: List all users (admin-only).
- `DELETE /delete_user/`: Delete a user by email (admin-only).
- `GET /Logs`: View admin activity logs (admin-only).

## 🏃 Running the Application

### 1. Start Redis
```
redis-server
```

### 2. Run the FastAPI Application
```
uvicorn main:app --reload
```

### 3. Start Celery Worker
```
celery -A Router.worker.celery_app worker --loglevel=info
```

### 4. Start Celery Beat (for scheduled tasks)
```
celery -A Router.worker.celery_app beat --loglevel=info
```

### 5. Access the API
- Swagger UI: http://localhost:8000/docs
- Test endpoint:
```
curl http://localhost:8000/test
```

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch:
```
git checkout -b feature-name
```
3. Commit your changes:
```
git commit -m "Add feature"
```
4. Push to the branch:
```
git push origin feature-name
```
5. Create a pull request.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
