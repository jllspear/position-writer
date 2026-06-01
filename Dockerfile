# Build stage
FROM python:3.13-slim-bullseye AS builder

WORKDIR /app

# Install system dependencies, including build tools required to compile hnswlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libpq5 \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache --extra standalone

# Runtime stage
FROM python:3.13-slim-bullseye AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
        postgresql-client \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy only necessary files
COPY --from=builder /app/alembic/ ./alembic/
COPY --from=builder /app/src/ ./src/
COPY --from=builder /app/main_standalone.py /app/entrypoint.sh /app/alembic.ini ./

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Default command (can be overridden)
CMD ["python", "-u", "main_standalone.py"]