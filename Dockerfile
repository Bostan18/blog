# 📰 Le Quotidien - Production Ready Dockerfile
# Optimized for size and security

# --- Stage 1: Build dependencies ---
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Stage 2: Final Image ---
FROM python:3.12-slim-bookworm

# Metadata
LABEL maintainer="Bostan18"
LABEL description="Le Quotidien - Plateforme d'Information Moderne"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/install/bin:$PATH"

WORKDIR /app

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /install /install

# Copy project files
COPY . .

# Static and Media folders permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chmod -R 755 /app/staticfiles /app/media

# Expose port
EXPOSE 8000

# Default command (overridden in docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
