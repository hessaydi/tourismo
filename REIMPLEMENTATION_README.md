# Tourismo - Travel Agency Management System (Reimplemented)

A complete reimplementation of the Tourismo Travel Agency Management System with a modern **FastAPI REST API** backend and a beautiful **React + TypeScript + Vite** frontend.

## 📋 Project Overview

This is a **full-stack microservice architecture** with:
- **Backend**: FastAPI (Python) REST API with SQLAlchemy ORM
- **Frontend**: React 18 with TypeScript and Vite
- **Database**: SQLite (development) / PostgreSQL (production)
- **UI Framework**: shadcn/ui + Tailwind CSS
- **Authentication**: JWT tokens
- **Containerization**: Docker & Docker Compose

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│  ├─ Pages (Dashboard, Packages, Clients, etc.)             │
│  ├─ Components (UI, Layout, Feature)                       │
│  ├─ Services (API Client, Auth Service)                    │
│  ├─ State (TanStack Query, React Context)                  │
│  └─ Styling (Tailwind CSS + Dark/Light Mode)               │
└─────────────────────────────────────────────────────────────┘
              ↓
          [REST API]
              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                         │
│  ├─ Routes (Auth, Users, Packages, etc.)                   │
│  ├─ Models (SQLAlchemy ORM)                                │
│  ├─ Schemas (Pydantic Validation)                          │
│  ├─ Services (Business Logic)                              │
│  └─ Security (JWT, RBAC, Password Hashing)                 │
└─────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────┐
│              Database (PostgreSQL/SQLite)                   │
│  ├─ Users                                                   │
│  ├─ Destinations, Packages                                 │
│  ├─ Clients, Bookings                                      │
│  ├─ Guides, Notifications                                  │
│  └─ [Relationships & Constraints]                          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Create environment files
cp backend-api/.env.example backend-api/.env
cp frontend/.env.example frontend/.env.local

# Start all services
docker-compose up -d

# Services will be available at:
# Frontend: http://localhost:5173
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Copy and configure .env
cp .env.example .env

# Run migrations (if using SQLAlchemy with Alembic)
# alembic upgrade head

# Start server
uvicorn app.main:app --reload
# API will be at http://localhost:8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy and configure .env
cp .env.example .env.local

# Start development server
npm run dev
# Frontend will be at http://localhost:5173
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Key Endpoints

**Authentication**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

**Resources**
- `/api/v1/destinations` - Destinations CRUD
- `/api/v1/packages` - Packages CRUD
- `/api/v1/clients` - Clients CRUD
- `/api/v1/bookings` - Bookings CRUD (with auto price calculation)
- `/api/v1/guides` - Guides CRUD
- `/api/v1/notifications` - Notifications management

See [Backend README](./backend-api/README.md) for complete API documentation.

## 🎨 Features

### ✅ Implemented

- [x] **Authentication System**
  - User registration and login
  - JWT token-based auth
  - Token refresh mechanism
  - Role-based access control (RBAC)

- [x] **Dashboard**
  - KPI statistics
  - Revenue and booking charts
  - Recent activity feed
  - Top packages listing

- [x] **Destinations Management**
  - List, create, update, delete destinations
  - Search and filter
  - Featured destinations

- [x] **Packages Management**
  - Full CRUD operations
  - Category-based filtering
  - Price management
  - Capacity tracking

- [x] **Clients Management**
  - Client profiles
  - Booking history
  - Passport and personal information
  - Contact details

- [x] **Bookings System**
  - Auto price calculation
  - Status tracking (pending, confirmed, etc.)
  - Payment status management
  - Booking reference generation
  - Special requests

- [x] **Guides Management**
  - Guide profiles
  - Languages and specialties
  - Rating system
  - Availability tracking

- [x] **Notifications**
  - User notifications
  - Read/unread status
  - Activity tracking

- [x] **Theme Support**
  - Dark mode
  - Light mode
  - Auto system preference

### 🔜 Future Enhancements

- [ ] Advanced filtering and search
- [ ] Booking confirmation emails
- [ ] Payment gateway integration
- [ ] Invoice generation
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Audit logging
- [ ] File upload (images for destinations)
- [ ] WebSocket notifications

## 🛠️ Tech Stack Comparison

### Old Architecture
- Django (Monolith)
- Server-rendered templates
- SQLite
- No type safety (Python)
- Tightly coupled

### New Architecture
- FastAPI (Microservice-ready)
- REST API with JSON
- SQLAlchemy ORM
- Full type safety (Python + TypeScript)
- Loosely coupled
- Modern React with hooks
- Built-in API documentation

## 📦 Project Structure

```
tourismo/
├── backend-api/              # FastAPI REST API
│   ├── app/
│   │   ├── main.py          # Application entry
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   ├── security.py      # JWT & Auth
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── routes/          # API endpoints
│   ├── pyproject.toml       # Dependencies
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                 # React + Vite
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── layouts/         # Layout components
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # API services
│   │   ├── contexts/        # React contexts
│   │   ├── types/           # TypeScript types
│   │   ├── utils/           # Utilities
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json         # Dependencies
│   ├── vite.config.ts       # Vite config
│   ├── tailwind.config.ts   # Tailwind config
│   ├── Dockerfile
│   └── README.md
│
├── docker-compose.yml       # Multi-container setup
└── README.md               # This file
```

## 🔒 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT tokens with expiration
- ✅ CORS protection
- ✅ Role-based access control
- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Secure token storage
- ✅ Automatic token refresh

## 📊 Database Schema

### Users
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(100) UNIQUE,
  email VARCHAR(255) UNIQUE,
  full_name VARCHAR(255),
  hashed_password VARCHAR(255),
  role VARCHAR(50), -- admin, manager, user
  is_active BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Additional Tables
- `destinations` - Travel destinations
- `packages` - Travel packages
- `clients` - Customer profiles
- `bookings` - Booking records with auto-calculated prices
- `guides` - Tour guides
- `notifications` - User notifications

See [Backend Models](./backend-api/app/models/) for full schema details.

## 🧪 Testing

### Backend Tests
```bash
cd backend-api
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm run type-check
```

## 🚀 Deployment

### Production Checklist
- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=false` in backend `.env`
- [ ] Configure PostgreSQL connection
- [ ] Set up SSL/TLS certificates
- [ ] Configure allowed hosts/CORS origins
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Run database migrations
- [ ] Build frontend for production
- [ ] Set up CI/CD pipeline

### Docker Production Build
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📖 Documentation

- [Backend Documentation](./backend-api/README.md)
- [Frontend Documentation](./frontend/README.md)
- [API Reference](./backend-api/README.md#-api-endpoints)
- [Architecture Guide](./docs/ARCHITECTURE.md) (Coming soon)
- [Deployment Guide](./docs/DEPLOYMENT.md) (Coming soon)

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Follow ESLint rules for TypeScript/React
- Write type hints/types for new functions
- Add tests for new features
- Update documentation

## 📝 Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Examples:
- `feat(auth): add JWT token refresh`
- `fix(api): correct booking price calculation`
- `docs(frontend): update component guide`
- `test(backend): add auth endpoint tests`

## 📄 License

This project is part of the Tourismo Travel Agency Management System.

## 🆘 Troubleshooting

### Backend won't start
1. Check Python version: `python --version` (need 3.11+)
2. Verify virtual environment: `source venv/bin/activate`
3. Reinstall dependencies: `pip install -e .`
4. Check port 8000 isn't in use: `lsof -i :8000`

### Frontend won't connect to API
1. Check API is running: `curl http://localhost:8000/health`
2. Verify `VITE_API_URL` in `.env.local`
3. Check browser console for CORS errors
4. Verify backend CORS_ORIGINS includes frontend URL

### Database connection issues
1. Check PostgreSQL is running (production)
2. Verify DATABASE_URL is correct
3. Check database credentials
4. For SQLite, ensure write permissions on directory

### Port conflicts
- Frontend default: 5173
- Backend default: 8000
- Database default: 5432
- Use `-p` flag to change ports if needed

## 📞 Support

- Issues: GitHub Issues
- Questions: GitHub Discussions
- Email: [your-email@domain.com]

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query)

---

**Status**: ✅ Ready for Development & Testing

**Last Updated**: August 2024

**Next Steps**: 
1. Install dependencies for both backend and frontend
2. Start development servers
3. Explore the API documentation at `/docs`
4. Begin feature development and testing
