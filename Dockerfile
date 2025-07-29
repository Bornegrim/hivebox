# ─────────────── Stage 1: Builder ───────────────
FROM python:3.13-slim@sha256:4c2cf9917bd1cbacc5e9b07320025bdb7cdf2df7b0ceaccb55e9dd7e30987419 AS builder

# Set environment variables to reduce image size and improve security
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential=12.9 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies into /install (we will copy this later)
RUN pip install --upgrade pip==24.3.1 \
    && pip install --prefix=/install -r requirements.txt

# ─────────────── Stage 2: Final ───────────────
FROM python:3.13-slim@sha256:4c2cf9917bd1cbacc5e9b07320025bdb7cdf2df7b0ceaccb55e9dd7e30987419

# Install curl for health check and create non-root user for security
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.1-10+deb12u12 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 hivebox \
    && useradd --uid 1000 --gid hivebox --shell /bin/bash --create-home hivebox

ENV PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.13/site-packages" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

COPY --from=builder /install /install
COPY ./app ./app

# Change ownership of the app directory to the non-root user
RUN chown -R hivebox:hivebox /app

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER hivebox

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]

