# syntax=docker/dockerfile:1.7-labs
FROM python:3.13-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Build stage
FROM base AS build
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN pip install --upgrade pip && \
    pip install . && \
    pip install "uvicorn[standard]"

# Runtime stage
FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000
WORKDIR /app

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=build /usr/local /usr/local
COPY --from=build /app/src /app/src

USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import requests,os; import sys; sys.exit(0 if requests.get(f'http://127.0.0.1:{os.getenv("PORT",8000)}/health',timeout=2).ok else 1)" || exit 1

CMD ["uvicorn", "ssdlc_demo.main:app", "--host", "0.0.0.0", "--port", "8000"] 