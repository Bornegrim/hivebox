# ─────────────── Stage 1: Builder ───────────────
FROM python:3.11.9-slim AS builder

# Set environment variables to reduce image size and improve security
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY requirements.txt .

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into /install (we will copy this later)
RUN pip install --upgrade pip==24.0 \
    && pip install --prefix=/install -r requirements.txt

# ─────────────── Stage 2: Final ───────────────
FROM python:3.11.9-slim

RUN adduser --disabled-password --gecos "" hiveboxuser

ENV PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.11/site-packages" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /install /install
COPY ./app ./app
COPY requirements.txt ./

USER hiveboxuser

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]

