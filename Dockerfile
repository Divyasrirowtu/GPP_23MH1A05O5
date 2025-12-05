# ---------- Stage 1: Builder (install Python deps) ----------
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies in one step, then clean cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libssl-dev libffi-dev python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install into a separate prefix
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

# Install runtime dependencies (cron + tzdata) in one layer, clean cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron tzdata \
 && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

# Ensure key/script permissions
RUN [ -f /app/student_private.pem ] && chmod 600 /app/student_private.pem || true \
 && [ -f /app/student_public.pem ] && chmod 644 /app/student_public.pem || true \
 && [ -f /app/instructor_public.pem ] && chmod 644 /app/instructor_public.pem || true \
 && [ -f /app/cron/2fa-cron ] && chmod 644 /app/cron/2fa-cron || true \
 && [ -f /app/entrypoint.sh ] && chmod +x /app/entrypoint.sh || true

# Volumes for persistent storage
VOLUME ["/data", "/cron"]

# Expose port required by evaluator
EXPOSE 8080

# Entrypoint starts cron + API
ENTRYPOINT ["/app/entrypoint.sh"]
