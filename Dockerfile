# ── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files and install into a virtual env
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the venv from builder
COPY --from=builder /app/.venv /app/.venv

# Install gunicorn and psycopg2 into the venv
RUN pip install --no-cache-dir gunicorn psycopg2-binary

# Copy project source
COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
