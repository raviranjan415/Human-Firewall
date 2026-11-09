# ==============================================================================
# Human Firewall — Multi-Stage Production Containerfile
# Hardened, Unprivileged, OCI-Compliant
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build & Dependency Wheel Cache
# ------------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /opt/venv/bin/pip install --no-cache-dir gunicorn psycopg[binary] redis

# ------------------------------------------------------------------------------
# Stage 2: Minimal Distroless-like Runtime
# ------------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS runner

LABEL maintainer="Human Firewall SecOps Team" \
      project="Human Firewall" \
      version="2.0.0" \
      description="Hardened Cybersecurity Awareness & Training Platform"

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000

# Install runtime dependencies (libpq for postgresql, curl for container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged application user and group (Principle of Least Privilege)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin -M -d /app appuser

# Copy virtualenv from builder stage
COPY --from=builder --chown=appuser:appgroup /opt/venv /opt/venv

# Copy application source code
COPY --chown=appuser:appgroup app /app/app
COPY --chown=appuser:appgroup run.py gunicorn.conf.py migrate_db.py /app/

# Create runtime directories for instance storage and logs with unprivileged ownership
RUN mkdir -p /app/instance /app/logs && \
    chown -R appuser:appgroup /app

USER 10001:10001

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:5000/healthz || exit 1

CMD ["gunicorn", "--config", "gunicorn.conf.py", "run:app"]

