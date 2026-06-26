# Tourismo — Travel Agency Management System

A full Django web application for managing a travel agency.

## Quick Start

```bash
pip install django
python manage.py migrate
python manage.py runserver
```
Then open http://127.0.0.1:8000

## Features

| Section | What you can do |
|---|---|
| **Dashboard** | KPIs, revenue chart, recent bookings |
| **Authentication** | Secure registration, login, and logout before dashboard access |
| **Role-Based Access** | Superuser/manager/normal permissions with user management controls |
| **Notifications** | In-app activity notifications with unread indicators |
| **Packages** | Create/edit travel packages with pricing & categories |
| **Bookings** | Full CRUD, auto price calc, status tracking |
| **Clients** | Client profiles, booking history, passport info |
| **Destinations** | Destination catalog with images |
| **Guides** | Guide profiles with languages and ratings |
| **Theme** | Refreshed UI with light and dark mode toggle |

## Stack
- Django 4+ · SQLite · Chart.js · Font Awesome
- No external CSS framework — custom responsive UI with theme switching

## Testing & Coverage

```bash
uv run pytest --cov=agency --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

The HTML coverage report is generated at `htmlcov/index.html`.
