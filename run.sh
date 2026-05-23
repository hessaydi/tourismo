#!/bin/bash
echo "=== Tourismo — Travel Agency Management System ==="
echo "Starting server at http://127.0.0.1:8000"
cd "$(dirname "$0")"
python manage.py runserver
