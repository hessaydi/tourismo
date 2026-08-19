# Tourismo REST API

A modern REST API for the Tourismo Travel Agency Management System built with FastAPI, SQLAlchemy, and PostgreSQL.

## 🚀 Features

- **FastAPI Framework**: Modern, fast, and easy to use
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Admin, Manager, and User roles
- **Complete CRUD Operations**: For all entities
- **Auto-Generated API Documentation**: Swagger UI and ReDoc
- **SQLAlchemy ORM**: Type-safe database queries
- **Pydantic Validation**: Strong data validation
- **Async/Await Support**: High-performance async operations

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### Destinations
- `GET /api/v1/destinations/` - List destinations
- `GET /api/v1/destinations/{id}` - Get destination
- `POST /api/v1/destinations/` - Create destination (admin/manager)
- `PUT /api/v1/destinations/{id}` - Update destination (admin/manager)
- `DELETE /api/v1/destinations/{id}` - Delete destination (admin)

### Packages
- `GET /api/v1/packages/` - List packages
- `GET /api/v1/packages/{id}` - Get package
- `POST /api/v1/packages/` - Create package (admin/manager)
- `PUT /api/v1/packages/{id}` - Update package (admin/manager)
- `DELETE /api/v1/packages/{id}` - Delete package (admin)

### Clients
- `GET /api/v1/clients/` - List clients
- `GET /api/v1/clients/{id}` - Get client
- `POST /api/v1/clients/` - Create client
- `PUT /api/v1/clients/{id}` - Update client
- `DELETE /api/v1/clients/{id}` - Delete client (admin/manager)

### Bookings
- `GET /api/v1/bookings/` - List bookings
- `GET /api/v1/bookings/{id}` - Get booking
- `POST /api/v1/bookings/` - Create booking (auto price calculation)
- `PUT /api/v1/bookings/{id}` - Update booking
- `DELETE /api/v1/bookings/{id}` - Delete booking (admin/manager)

### Guides
- `GET /api/v1/guides/` - List guides
- `GET /api/v1/guides/{id}` - Get guide
- `POST /api/v1/guides/` - Create guide (admin/manager)
- `PUT /api/v1/guides/{id}` - Update guide (admin/manager)
- `DELETE /api/v1/guides/{id}` - Delete guide (admin)

### Notifications
- `GET /api/v1/notifications/` - List user notifications
- `GET /api/v1/notifications/{id}` - Get notification
- `POST /api/v1/notifications/` - Create notification (admin/manager)
- `PUT /api/v1/notifications/{id}` - Update notification
- `DELETE /api/v1/notifications/{id}` - Delete notification
- `POST /api/v1/notifications/{id}/mark-as-read` - Mark as read

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104+
- **Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: JWT with python-jose
- **Validation**: Pydantic 2.0+
- **Testing**: pytest + pytest-asyncio

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Setup

1. **Clone the repository**
   ```bash
   cd backend-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   # or with uv:
   uv sync
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🧪 Testing

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

## 🐳 Docker

Build and run with Docker:
```bash
docker build -t tourismo-api .
docker run -p 8000:8000 tourismo-api
```

With Docker Compose:
```bash
docker-compose up -d
```

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `true` | Enable debug mode |
| `SECRET_KEY` | - | JWT secret key (change in production) |
| `DATABASE_URL` | `sqlite:///./tourismo.db` | Database connection string |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed CORS origins |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |

## 🔐 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS protection enabled
- Role-based access control (RBAC)
- Input validation with Pydantic

## 📄 License

This project is part of the Tourismo Travel Agency Management System.

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Submit a pull request

## 📞 Support

For issues and questions, please open an issue in the repository.
