# Step - 1: Builder
FROM python:3.13-slim as builder

WORKDIR /app

# Install system build dependencies (gcc, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to a specific location
COPY requirements.txt .
# If you are using uv, you can export requirements or use uv here.
# Assuming standard pip for broad compatibility in the final stage:
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Step - 2: Runtime
#Use official lightweight Python image
FROM python:3.13-slim

# Install runtime libs for Postgres (libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from Builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]